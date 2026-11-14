"""global-law has no replay of serbia-law yet, so the history detectors had nothing to read for Serbia. This adds the
same rows global-law's replay would give, from serbia-law's own commit trailers (Law, Kind, In-force)."""
import duckdb
con = duckdb.connect()
con.sql("""
create table s as
select commit as root, corpus, commit as corpus_commit,
       json_extract_string(trailers, '$.Law[0]') as law,
       regexp_extract(json_extract_string(trailers, '$."In-force"[0]'), '\d{4}-\d{2}-\d{2}') as in_force,
       json_extract_string(trailers, '$.Kind[0]') as kind,
       'Serbia: ' || subject as subject
from 'index/commits/serbia-law.parquet'
where json_extract_string(trailers, '$.Kind[0]') is not null""")
print(con.sql("select kind, count(*) from s group by 1 order by 2 desc").fetchall())
con.sql("""copy (select * from 'index/root.parquet' where corpus <> 'serbia/national/acts' union all select * from s)
           to 'index/root.new.parquet' (format parquet, compression zstd)""")
