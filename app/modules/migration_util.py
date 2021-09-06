__license__ = "MIT"
__copyright__ = "Copyright 2020, Konrad Mohrfeldt"
# originally from https://gist.github.com/kmohrf/3989eee63243f895396beffc61668e07

from functools import partial
from typing import Callable, Iterable, Union

from django.db import migrations
from django.db.migrations.state import StateApps
from django.db.models.base import ModelBase
from wagtail.core.blocks.stream_block import StreamValue


def migrate_streamfield_name(
    model_resolver: Callable[[StateApps], ModelBase],
    attributes: Union[str, Iterable[str]],
    old_name: str,
    new_name: str,
    fields: dict,
) -> migrations.RunPython:
    """Creates a migration that converts the name used for a block inside a Wagtail StreamField.
    If you have a StreamField definition that looks like this:
        body = StreamField([
            ("paragraph", blocks.RichTextBlock()),
            ("custom_block", MyCustomBlock()),
        })
    and you want to change the name of "custom_block" to "custom_schmock" this will do the job.
    Example:
        migrate_streamfield_name(lambda apps: apps.get_model("my_app.MyModel"),
                                 "body", "custom_block", "custom_schmock", {"old_field": "new_field"})
    :param model_resolver: a callable that returns the Model class for which the migration should be executed
    :param attributes: the name (or an iterable of names) of the StreamField(s) attributes that should be migrated
    :param old_name: the name for the block type that was used until now ("custom_block" in the example)
    :param new_name: the name for the block type that should be used from now on ("custom_schmock" in the example)
    :param fields: rename fields from key to value
    :return: Up- and down-migration for the model
    """

    def migrate_fields(original_dict, lookup, reverse=False):
        """this'll break horribly if both lists contain the same names for different fields"""
        for k, v in lookup.items():
            if reverse:
                new_name, old_name = k, v
            else:
                old_name, new_name = k, v
            original_dict[new_name] = original_dict[old_name]
            del original_dict[old_name]
        return original_dict

    def migrate(apps, schema_editor, old_name, new_name, fields=None, reverse=False):
        db_alias = schema_editor.connection.alias
        Model = model_resolver(apps)
        objects = Model.objects.using(db_alias).all()
        for obj in objects:
            has_modified_model = False
            for attr in attributes:
                has_modified_attr = False
                migrated_stream_data = []
                attr_value = getattr(obj, attr)  # a 'StreamValue'
                """contains: append, clear, count, extend, get_prep_value, index, insert, is_lazy,
                pop, raw_data, raw_text, remove, render_as_block, reverse, stream_block"""
                for data in attr_value.raw_data:  # was stream_data
                    print(data)
                    if data["type"] == old_name:
                        has_modified_model = has_modified_attr = True

                        migrated_stream_data.append(
                            {
                                "type": new_name,
                                "value": migrate_fields(
                                    data["value"], lookup=fields, reverse=reverse
                                ),
                            }
                        )
                    else:
                        migrated_stream_data.append(data)
                if has_modified_attr:
                    new_data = StreamValue(
                        attr_value.stream_block, migrated_stream_data, is_lazy=True
                    )
                    setattr(obj, attr, new_data)
            if has_modified_model:
                obj.save()

    if isinstance(attributes, str):
        attributes = {attributes}
    return migrations.RunPython(
        code=partial(
            migrate, old_name=old_name, new_name=new_name, fields=fields, reverse=False
        ),
        reverse_code=partial(
            migrate, old_name=new_name, new_name=old_name, fields=fields, reverse=True
        ),
    )
