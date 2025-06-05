USE airport;

CREATE OR REPLACE FUNCTION duration_ms(arr timestamp, dep timestamp)
RETURNS NULL ON NULL INPUT
RETURNS bigint
LANGUAGE java AS '
    return Long.valueOf(arr.getTime() - dep.getTime());
';
