set -U fish_term24bit 1
set -U fish_color_search_match 'fff'
set -U fish_color_error 'f99'
set -U fish_color_autosuggestion '999'
set -U fish_color_valid_path  # Remove underlines on paths
set -U fish_color_command '39d'

function fish_prompt

  if [ $SERVER_ENV = 'development' ]
    set_color -b '00a600'
    set_color '000'
  else if [ $SERVER_ENV = 'staging' ]
    set_color -b 'd8b500'
    set_color '000'
  else if [ $SERVER_ENV = 'production' ]
    set_color -b 'e60000'
    set_color 'fff'
  else
    set_color -b 999
  end

  printf ' '
  printf $SERVER_ENV
  printf ' '

  set_color -b normal
  set_color yellow
  printf ' ➜ '
  set_color cyan
  printf (basename $PWD)
  printf ' 🐟 '
  set_color normal
end


function static_app
  if [ (count $argv) = 0 ]
    echo "pass either staging or production to the static call"
    exit 1
  end
  export SERVER_ENV=$argv
  python manage.py assets clean
  python manage.py assets build
  python manage.py collectstatic --no-input -v 2 -i node_modules -i admin -i 'django**' -i 'wagtail**' -i _dev
  export SERVER_ENV=development
end

function static
    if [ (count $argv) = 0 ]
      echo "pass either staging or production to the static call"
      exit 1
    end
    export SERVER_ENV=$argv
    python manage.py assets clean
    python manage.py assets build
    python manage.py collectstatic --no-input -v 2 -i node_modules
    export SERVER_ENV=development
end

function fish_greeting
    echo ""
    echo "🐟 Installed aliases..."
    echo "runserver - Runs the development server on port 5000"
    echo "sp - Runs python manage.py shell_plus"
    echo "manpy - Shorthand for python manage.py"
    echo ""
end


alias runserver="python manage.py runserver 0.0.0.0:5000"
alias sp="python manage.py shell_plus"
alias manpy="python manage.py"

eval (envkey-source)
source $HOME/.poetry/env


# If there's an activate.fish file, then source it
if [ -e ".venv/bin/activate.fish" ]
    source .venv/bin/activate.fish
end
