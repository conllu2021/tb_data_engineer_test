COPY (
    SELECT *
    FROM
        read_parquet('{input_file}')
    QUALIFY
        ntile(100) OVER (ORDER BY trip_distance) >= {percentile}
)
TO '{output_file}' (FORMAT parquet)
