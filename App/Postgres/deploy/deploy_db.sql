drop table if exists file_library;

create table if not exists file_library
(
    id                        serial,
    file_name                 varchar not null,
    audio_path                varchar not null,
    create_time               timestamp not null,
    duration                  int not null,
    diarization               json default null,
    full_text_path            varchar default null,
    official_summary_path     varchar default null,
    unofficial_summary_path   varchar default null,
    speaker_mapping           json default null,
    document                  json default null,
    status                    varchar not null
);
