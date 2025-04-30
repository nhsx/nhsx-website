# stdlib
import os

# 3rd party
from django.urls import path
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from wagtail.core import views as wagtail_views
from wagtail.admin import urls as wagtailadmin_urls
from django.contrib import admin
from django.conf.urls import url, include
from wagtail.core.urls import WAGTAIL_FRONTEND_LOGIN_TEMPLATE, serve_pattern
from wagtail.documents import urls as wagtaildocs_urls
from wagtailcache.cache import cache_page
from django.contrib.auth import views as auth_views
from wagtail.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

# Project
from modules.search import views as search_views
from modules.core.views import AuthorAutocomplete


PROD_ROBOTS = """
User-agent: *
Disallow: /admin/

User-agent: *
Allow: /

Sitemap: https://nhsx.nhs.uk/sitemap.xml
"""


def robots(request):
    server_env = os.environ.get("SERVER_ENV")
    if server_env == "production" or server_env == "development":
        return HttpResponse(PROD_ROBOTS, content_type="text/plain")
    else:
        return HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")


urlpatterns = [
    url(r"^django-admin/", admin.site.urls),
    url(r"^admin/", include(wagtailadmin_urls)),
    url(r"^documents/", include(wagtaildocs_urls)),
    url(r"^search/$", search_views.search, name="search"),
    url(r"^sitemap\.xml$", sitemap),
    url(r"^robots\.txt$", robots),
    url(
        r"^author-autocomplete/$",
        AuthorAutocomplete.as_view(),
        name="author-autocomplete",
    ),
    url(
        r"^analytics\.txt",
        TemplateView.as_view(template_name="analytics.txt", content_type="text/plain"),
    ),
    #
    # 301 redirects.
    #
    # https://dxw.zendesk.com/agent/tickets/17352
    url(
        r"^improvement/focusondiagnostics/",
        lambda request: redirect(r"/focusondiagnostics/", permanent=True),
    ),
    # https://dxw.zendesk.com/agent/tickets/17538
    url(
        r"^key-tools-and-info/get-started-with-nhsx-digital-and-technology-assurance/",
        lambda request: redirect(
            r"/key-tools-and-info/get-started-with-digital-and-technology-assurance/",
            permanent=True,
        ),
    ),
    # https://dxw.zendesk.com/agent/tickets/17711
    url(
        r"^covid-19-response/technology-nhs/supporting-transformation-through-innovation-collaborative/",
        lambda request: redirect(
            r"/covid-19-response/technology-nhs/innovation-collaborative-for-digital-health/",
            permanent=True,
        ),
    ),
    url(
        r"^covid-19-response/technology-nhs/the-nhsx-national-innovation-collaborative-podcast/",
        lambda request: redirect(
            r"/covid-19-response/technology-nhs/the-innovation-collaborative-podcast/",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/regulating-the-ai-ecosystem/the-multi-agency-advice-service-maas/",
        lambda request: redirect(
            r"/ai-lab/ai-lab-programmes/regulating-the-ai-ecosystem/the-ai-and-digital-regulations-service/",
            permanent=True,
        ),
    ),
    # https://dxw.zendesk.com/agent/tickets/18089
    url(
        r"^information-governance/ig-question-time/",
        lambda request: redirect(
            r"/information-governance/frequently-asked-questions/",
            permanent=True,
        ),
    ),
    # https://dxw.zendesk.com/agent/tickets/19293
    url(
        r"^key-tools-and-info/data-saves-lives/accessing-data-for-research-and-analysis/",
        lambda request: redirect(
            r"/key-tools-and-info/data-saves-lives/secure-data-environments/accessing-data-for-research-and-analysis/",
            permanent=True,
        ),
    ),
    url(
        r"^key-tools-and-info/data-saves-lives/accessing-data-for-research-and-analysis/work-in-progress/",
        lambda request: redirect(
            r"/key-tools-and-info/data-saves-lives/secure-data-environments/how-will-secure-data-environments-be-delivered/",
            permanent=True,
        ),
    ),
    # https://dxw.zendesk.com/agent/tickets/20062
    url(
        r"^information-governance/health-and-care-information-governance-panel/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052114/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/about-health-and-care-ig-panel/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052119/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/about-health-and-care-ig-panel/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/people/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052102/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/people/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/people/dame-fiona-caldicott/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052102/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/people/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/people/ian-hulme/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052102/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/people/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/people/jackie-gray/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052102/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/people/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/people/edward-morris/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052102/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/people/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/people/dr-tony-calland/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052102/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/people/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/people/dawn-monaghan/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052102/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/people/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/people/andrew-hughes/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052102/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/people/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/people/elizabeth-bohm/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052102/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/people/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/people/simon-richardson/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052102/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/people/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/2019-10-10/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/2020-01-28/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/2020-03-11/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/2020-07-28/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/2020-09-15/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/2020-11-26/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/2021-03-24/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/2021-05-18/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/2021-07-20/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/2021-11-23/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/2022-03-22/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    url(
        r"^information-governance/health-and-care-information-governance-panel/minutes/2022-05-24/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20240501052022/https://transform.england.nhs.uk/information-governance/health-and-care-information-governance-panel/minutes/",
            permanent=True,
        ),
    ),
    # https://dxw.zendesk.com/agent/tickets/20390
    url(
        r"^key-tools-and-info/digital-transformation-of-screening/",
        lambda request: redirect(
            r"/key-tools-and-info/digital-screening/",
            permanent=True,
        ),
    ),
    # https://dxw.zendesk.com/agent/tickets/20832
    url(
        r"^ai-lab/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/about-the-nhs-ai-lab/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/about-the-nhs-ai-lab/nhs-ai-lab-get-involved/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/about-the-nhs-ai-lab/2020-21-a-year-in-the-life-of-the-nhs-ai-lab/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/adopt-ai/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/adopt-ai/a-buyers-guide-to-ai-in-health-and-care/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/adopt-ai/a-buyers-guide-to-ai-in-health-and-care/a-buyers-guide-to-ai-in-health-and-care/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/adopt-ai/a-buyers-guide-to-ai-in-health-and-care/ai-buyers-guide-assessment-template/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/adopt-ai/clinical-trial-protocols-spirit-ai-extension/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/adopt-ai/assessing-if-ai-right-solution/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/adopt-ai/understanding-ai-ethics-and-safety/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/adopt-ai/guidelines-ai-procurement/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/adopt-ai/preparing-healthcare-workforce-deliver-digital-future/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/adopt-ai/healthtechconnect/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/adopt-ai/guide-using-ai-public-sector/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/examining-whether-recruitment-data-can-and-should-be-used-to-train-ai-models-for-shortlisting-interview-candidates/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/case-studies",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/working-with-a-trusted-research-environment/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/case-studies",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/identifying-and-quantifying-parkinsons-disease-using-ai-on-brain-slices/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/case-studies",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/using-deep-learning-to-detect-adrenal-lesions-in-ct-scans/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/case-studies",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/ai-regulation-guide-using-pico-to-generate-evidence-for-ai-development/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/ai-regulation-guide-considerations-when-developing-ai-products-and-tools/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/using-ai-to-find-optimal-placement-schedules-for-nursing-students/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/case-studies",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/exploring-how-to-create-mock-patient-data-synthetic-data-from-real-patient-data/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/case-studies",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/nccid-case-study-setting-standards-for-testing-artificial-intelligence/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/using-machine-learning-to-identify-patients-at-risk-of-long-term-hospital-stays/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20241101054858/https://transform.england.nhs.uk/ai-lab/explore-all-resources/develop-ai/using-machine-learning-to-identify-patients-at-risk-of-long-term-hospital-stays/",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/evidence-standards-framework/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/good-machine-learning-practice-for-medical-device-development-guiding-principles/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/ai-in-imaging-resource-collection/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/bayesboost-identifying-and-handling-bias-using-synthetic-data-generators/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/generating-and-evaluating-cross-sectional-synthetic-electronic-healthcare-data/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/practical-lessons-from-generating-synthetic-healthcare-data-with-bayesian-networks/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/generating-high-fidelity-synthetic-patient-data-for-assessing-machine-learning-healthcare-software/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/algorithmic-impact-assessment-a-case-study-in-healthcare/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/towards-nationally-curated-data-archives-for-clinical-radiology-image-analysis-at-scale/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/an-overview-of-the-national-covid-19-chest-imaging-database-data-quality-and-cohort-analysis/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/explainability-data-driven-health-and-care-technology/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/improving-hospital-bed-allocation-using-ai/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20241101060022/https://transform.england.nhs.uk/ai-lab/explore-all-resources/develop-ai/improving-hospital-bed-allocation-using-ai/",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/blog-lessons-learned-from-the-multi-agency-advisory-service-helping-developers-of-ai-and-data-driven-tech-to-navigate-the-regulatory-pathway/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/using-ai-to-identify-tissue-growth-from-ct-scans/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20241101055214/https://transform.england.nhs.uk/ai-lab/explore-all-resources/develop-ai/using-ai-to-identify-tissue-growth-from-ct-scans/",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/digital-technology-assessment-criteria-dtac/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/ai-in-imaging/ai-diagnostic-fund/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/ai-award-research-contract/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/ai-award-research-contract/ai-award-funding-agreement-phases-3-and-4/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/data-lens-a-fast-access-data-search-in-multiple-languages/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20241101060541/https://transform.england.nhs.uk/ai-lab/explore-all-resources/develop-ai/data-lens-a-fast-access-data-search-in-multiple-languages/",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/code-conduct-data-driven-health-and-care-technology/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/evidence-standards-framework-digital-health-technologies/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/develop-ai/project-explain/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/develop-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/artificial-intelligence-ai-funding-streams/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/understanding-ai-regulation/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/using-ai-to-improve-back-office-efficiency-in-the-nhs/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/case-studies",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/sharing-ai-skills-and-experience-through-deep-dive-workshops/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/case-studies",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/artificial-intelligence-how-get-it-right/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/artificial-intelligence-how-get-it-right/artificial-intelligence-how-to-get-it-right/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/creating-international-approach-ai-healthcare/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/ai-adult-social-care/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/user-centred-service-design-free-text-analytics/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/using-ai-to-support-nhs-resolution-with-negligence-claims-prediction/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20241101055118/https://transform.england.nhs.uk/ai-lab/explore-all-resources/understand-ai/using-ai-to-support-nhs-resolution-with-negligence-claims-prediction/",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/intelligent-monitoring-proactive-care/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/remote-intelligent-monitoring-and-predictive-analytics-support-people-their-optimal-care-setting/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/acoustic-monitoring-integrated-electronic-care-planning/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/nhs-ai-lab-1st-anniversary-event/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/analytics-and-decision-support-improve-workforce-retention/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/decision-support-care-workers-about-their-next-best-actions/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/smart-box-boosts-regional-data-to-the-nccid/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/mia-mammography-intelligent-assessment/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/healthyio-smartphone-albuminuria-urine-self-testing/",
        lambda request: redirect(
            r"https://transform.england.nhs.uk/ai-lab/explore-all-resources/understand-ai/healthyio-smartphone-albuminuria-urine-self-testing/",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/precision-medicine/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/emrad/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20241101055905/https://transform.england.nhs.uk/ai-lab/explore-all-resources/understand-ai/emrad/",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/kortical/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20241101055911/https://transform.england.nhs.uk/ai-lab/explore-all-resources/understand-ai/kortical/",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/cogstack/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20241101055244/https://transform.england.nhs.uk/ai-lab/explore-all-resources/understand-ai/cogstack/",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/how-data-supporting-covid-19-response/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20241101052929/https://transform.england.nhs.uk/covid-19-response/data-and-covid-19/how-data-supporting-covid-19-response/",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/european-respiratory-journal-using-imaging-combat-pandemic/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/predictive-analytics-assess-risk-and-trigger-care-interventions/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/remote-monitoring-vital-signs/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/remote-monitoring-early-detection-respiratory-conditions/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/assessing-pain-people-dementia-who-cannot-self-report/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/predictive-analytics-responding-post-covid-19-world/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/matching-demand-social-support-supply-through-geospatial-mapping-and-digital-marketplace/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/proactive-intervention-through-predictive-analytics/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/joined-demand-analysis-health-and-care/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/proactive-intervention-through-predictive-analytics/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/machine-learning-diagnostic-and-screening-services/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/data-driven-healthcare-regulation-regulators/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/industrial-strategy-ai-mission/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/dstl-biscuit-book/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/cdei-ai-barometer/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository/understand-ai",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/ai-health-and-care-award/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/ai-health-and-care-award/ai-health-and-care-award-winners/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20241101053812/https://transform.england.nhs.uk/ai-lab/ai-lab-programmes/ai-health-and-care-award/ai-health-and-care-award-winners/",
            permanent=True,
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/skunkworks/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/skunkworks/ai-skunkworks-projects/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/ethics/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/regulating-the-ai-ecosystem/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/regulating-the-ai-ecosystem/the-ai-and-digital-regulations-service/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/the-national-strategy-for-ai-in-health-and-social-care/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/the-national-strategy-for-ai-in-health-and-social-care/surveying-public-perceptions-of-ai/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/the-national-strategy-for-ai-in-health-and-social-care/understanding-the-digital-health-landscape/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/the-national-strategy-for-ai-in-health-and-social-care/ai-strategy-resources/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/ai-in-imaging/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/ai-in-imaging/ai-deployment-platform/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/ai-in-imaging/ai-imaging-what-we-do/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/ai-in-imaging/nccid-privacy-notice/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/ai-in-imaging/engaging-with-you-about-the-nccid/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/ai-in-imaging/how-patient-data-is-used-in-the-nccid/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-virtual-hub/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/nhs-ai-lab-roadmap/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/ai-lab-programmes/ai-in-imaging/",
        lambda request: redirect(
            r"https://digital.nhs.uk/services/ai-knowledge-repository", permanent=True
        ),
    ),
    url(
        r"^ai-lab/explore-all-resources/understand-ai/kortical/",
        lambda request: redirect(
            r"https://webarchive.nationalarchives.gov.uk/ukgwa/20241101055911/https://transform.england.nhs.uk/ai-lab/explore-all-resources/understand-ai/kortical/",
            permanent=True,
        ),
    ),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Add views for testing 404 page
    urlpatterns += [
        path("test-404/", TemplateView.as_view(template_name="404.html")),
    ]

urlpatterns = urlpatterns + [
    url(
        r"^_util/authenticate_with_password/(\d+)/(\d+)/$",
        wagtail_views.authenticate_with_password,
        name="wagtailcore_authenticate_with_password",
    ),
    url(
        r"^_util/login/$",
        auth_views.LoginView.as_view(template_name=WAGTAIL_FRONTEND_LOGIN_TEMPLATE),
        name="wagtailcore_login",
    ),
    # Wrap the serve function with wagtail-cache
    url(serve_pattern, cache_page(wagtail_views.serve), name="wagtail_serve"),
]
