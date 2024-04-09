> [!WARNING]
> 
> Przed uruchomieniem programu należy utworzyć plik .env
> 
## Przykładowa zawartość pliku .env


>
> POSTGRES_DB=<db_name>
>
> POSTGRES_USER=<db_user>
>
> POSTGRES_PASSWORD=<db_password>
>
> POSTGRES_PORT=<db_port>
>
> 
> SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}
>
> 
> SECRET_KEY=<secret_key>
> ALGORITHM=<algorithm>
>
> MAIL_USERNAME=<mail_username>
>
> MAIL_PASSWORD=<mail_password>
> 
> MAIL_FROM=<mail_from>
> 
> MAIL_PORT=<mail_port>
> 
> MAIL_SERVER=<mail_server>
> 
> MAIL_FROM_NAME=<mail_from_name>
>
