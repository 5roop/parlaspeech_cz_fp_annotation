import polars as pl
from pathlib import Path

pl.Config.set_tbl_cols(-1)
pl.Config.set_tbl_rows(300)
pl.Config.set_tbl_width_chars(200)
pl.Config.set_fmt_str_lengths(100)
df = (
    pl.read_ndjson("ParlaSpeech-CZ.v1.0.jsonl")
    .rename(
        {
            "audio_length": "duration",
            "id": "ident",
            "audio": "audio_file",
        }
    )
    .with_columns(
        pl.col("words").list.len().alias("w_count"),
        pl.col("words").list.first().struct.field("id").alias("start"),
        pl.col("words").list.last().struct.field("id").alias("end"),
        pl.lit(0.0).alias("start_s"),
        pl.col("speaker_info").struct.field("Speaker_ID").alias("who"),
        pl.lit("ParlaSpeech-CZ.v1.0.jsonl").alias("path"),
        pl.lit("ParlaSpeech-CZ.v1.0.jsonl").alias("filename"),
    )
    .with_columns(
        (pl.col("start_s") + pl.col("duration")).round(3).alias("end_s"),
        pl.col("audio_file")
        .map_elements(lambda s: Path(s).exists(), return_dtype=pl.Boolean)
        .alias("file_exists"),
    )
).select(
    [
        "ident",
        "who",
        "start",
        "start_s",
        "end",
        "end_s",
        "w_count",
        "path",
        "filename",
        "duration",
        "audio_file",
        "file_exists",
    ]
)

print(df["file_exists"].value_counts())
df.select(pl.exclude("file_exists")).write_ndjson("1_utterances.jsonl")
2 + 2
