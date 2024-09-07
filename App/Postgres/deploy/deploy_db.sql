drop table file_library;

create table if not exists file_library
(
    id                        serial,
    file_name                 varchar,
    raw_audio_path            varchar,
    full_text_path            varchar,
    official_summary_path     varchar,
    unofficial_summary_path   varchar,
    speaker_mapping           json
);