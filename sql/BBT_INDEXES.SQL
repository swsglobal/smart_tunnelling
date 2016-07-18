CREATE INDEX BbtParameterEval_TunnelName ON BbtParameterEval (tunnelName);
CREATE INDEX BbtParameterEval_TbmName ON BbtParameterEval (tbmName);
CREATE INDEX BbtParameterEval_ProfiloId ON BbtParameterEval (profilo_id);
CREATE INDEX BbtTbmKpi_TunnelName ON BbtTbmKpi (tunnelName);
CREATE INDEX BbtTbmKpi_TbmName ON BbtTbmKpi (tbmName);
CREATE INDEX BbtTbmKpi_KpiKey ON BbtTbmKpi (kpiKey);
create index BbtParameterEval_tunneliteration on BbtParameterEval (tunnelname, iteration_no);
create index BbtParameterEval_tunneltbm on BbtParameterEval (tunnelname, tbmname);