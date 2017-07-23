# Advanced Configuration

Praelatus supports configuration through environment variables as well as a
config.yaml file in the data directory. Some configuration can only be done
through environment variables so we suggest reading the following table to see
the available options, for most users the defaults will be sufficient.
A detailed explanation of each option will follow.

| Environment Variable          | Config.yaml Key                | Default Value                                 |
|:-----------------------------:|:------------------------------:|:---------------------------------------------:|
| PRAE_DATA_DIR                 | None                           | $PRAELATUS_INSTALL_DIR/data                   |
| PRAE_DEBUG                    | debug                          | False                                         |
| PRAE_ALLOWED_HOSTS            | allowed_hosts                  | $HOST                                         |
| PRAE_SESSION_ENGINE           | session_engine                 | 'django.contrib.sessions.backends.cached_db'  |
| PRAE_DB_ENGINE                | database -> default -> ENGINE  | 'django.db.backends.postgresql'               |
| PRAE_DB_NAME                  | database -> default -> NAME    | 'praelatus'                                   |
| PRAE_DB_USER                  | database -> default -> USER    | 'postgres'                                    |
| PRAE_DB_PASS                  | database -> default -> PASS    | 'postgres'                                    |
| PRAE_DB_HOST                  | database -> default -> HOST    | '127.0.0.1'                                   |
| PRAE_DB_PORT                  | database -> default -> PORT    | '5432'                                        |
| PRAE_LANG_CODE                | language_code                  | 'en-us'                                       |
| PRAE_TZ                       | time_zone                      | 'UTC'                                         |
| PRAE_USE_TZ                   | use_tz                         | 'true'                                        |
| PRAE_USE_INTERNATIONALIZATION | use_i18n                       | 'true'                                        |
| PRAE_STATIC_ROOT              | static_root                    | $PRAE_DATA_DIR/static                         |
| PRAE_MEDIA_ROOT               | media_root                     | $PRAE_DATA_DIR/media                          |
| None                          | cache -> default -> BACKEND    | 'django_redis.cache.RedisCache'               |
| None                          | cache -> default -> KEY_PREFIX | 'PRAE'                                        |
| PRAE_REDIS_URL                | cache -> default -> LOCATION   | 'redis://127.0.0.1:6379/1'                    |
| PRAE_MQ_SERVER                | mq_server                      | 'amqp://guest:guest@localhost:5672//'         |
| PRAE_MQ_RESULT                | mq_result_backend              | 'rpc://'                                      |
| PRAE_EMAIL_BACKEND            | email -> backend               | 'django.core.mail.backends.smtp.EmailBackend' |
| PRAE_EMAIL_ADDRESS            | email -> address               | 'praelatus@$HOST'                             |
| PRAE_EMAIL_HOST               | email -> host                  | 'localhost'                                   |
| PRAE_EMAIL_PORT               | email -> port                  | '25'                                          |
| PRAE_EMAIL_USER               | email -> user                  | None                                          |
| PRAE_EMAIL_PASS               | email -> pass                  | None                                          |
| PRAE_EMAIL_USE_TLS            | email -> use_tls               | False                                         |
| PRAE_EMAIL_USE_SSL            | email -> use_ssl               | False                                         |


