BEGIN TRANSACTION;
CREATE TABLE `test` (
	`keyp`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`val1`	REAL,
	`val2`	NUMERIC
);
CREATE TABLE BbtTbmKpi (
                        tunnelName STRING,
                        tbmName STRING,
                        iterationNo INTEGER,
                        kpiKey REAL,
                        kpiDescr REAL,
                        minImpact REAL,
                        maxImpact REAL,
                        avgImpact REAL,
                        appliedLength REAL,
                        percentOfApplication REAL,
                        probabilityScore REAL,
                        totalImpact REAL
);
CREATE TABLE BbtTbm (
	name TEXT NOT NULL PRIMARY KEY,
	alignmentCode TEXT,
	manufacturer TEXT,
	type TEXT,
	shieldLength REAL,
	overcut REAL
, breakawayTorque);
CREATE TABLE "BbtReliability" (
	`keyp`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`id`	INTEGER,
	`inizio`	REAL,
	`fine`	REAL,
	`gmr_class`	REAL,
	`gmr_val`	REAL,
	`reliability`	REAL,
	`eval_var`	REAL
);
CREATE TABLE "BbtProfilo" (
	`keyp`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`inizio`	REAL,
	`fine`	REAL,
	`est`	REAL,
	`nord`	REAL,
	`he`	REAL,
	`hp`	REAL,
	`co`	REAL,
	`tipo`	TEXT,
	`id`	INTEGER,
	`wdepth`	REAL
);
CREATE TABLE "BbtParameterEval" (
	`keyp`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`insertdate`	STRING,
	`iteration_no`	INTEGER,
	`fine`	REAL,
	`he`	REAL,
	`hp`	REAL,
	`co`	REAL,
	`gamma`	REAL,
	`sigma`	REAL,
	`mi`	REAL,
	`ei`	REAL,
	`cai`	REAL,
	`gsi`	REAL,
	`rmr`	REAL,
	`pkgl`	REAL,
	`closure`	REAL,
	`rockburst`	REAL,
	`front_stability_ns`	REAL,
	`front_stability_lambda`	REAL,
	`penetrationRate`	REAL,
	`penetrationRateReduction`	REAL,
	`contactThrust`	REAL,
	`torque`	REAL,
	`frictionForce`	REAL,
	`requiredThrustForce`	REAL,
	`availableThrust`	REAL,
	`dailyAdvanceRate`	REAL,
	`profilo_id`	INTEGER,
	`geoitem_id`	INTEGER,
	`title`	TEXT,
	`sigma_ti`	REAL,
	`k0`	REAL,
	`t0`	REAL,
	`t1`	REAL,
	`t3`	REAL,
	`t4`	REAL,
	`t5`	REAL,
	`tunnelName`	TEXT,
	`tbmName`	TEXT,
	`inSituConditionSigmaV`	REAL,
	`tunnelRadius`	REAL,
	`rockE`	REAL,
	`mohrCoulombPsi`	REAL,
	`rockUcs`	REAL,
	`inSituConditionGsi`	REAL,
	`hoekBrownMi`	REAL,
	`hoekBrownD`	REAL,
	`hoekBrownMb`	REAL,
	`hoekBrownS`	REAL,
	`hoekBrownA`	REAL,
	`hoekBrownMr`	REAL,
	`hoekBrownSr`	REAL,
	`hoekBrownAr`	REAL,
	`urPiHB`	REAL,
	`rpl`	REAL,
	`picr`	REAL,
	`ldpVlachBegin`	REAL,
	`ldpVlachEnd`	REAL,
	`wdepth`	REAL,
	`sigma_v_max_tail_skin`	REAL,
	`sigma_h_max_tail_skin`	REAL,
	`sigma_v_max_front_shield`	REAL,
	`sigma_h_max_front_shield`	REAL,
	`overcut_required`	INTEGER,
	`auxiliary_thrust_required`	INTEGER,
	`consolidation_required`	INTEGER,
	`sigma_h_max_lining`	REAL,
	`sigma_v_max_lining`	REAL,
	`anidrite`	REAL
);
CREATE TABLE "BbtParameter" (
	`keyp`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`inizio`	REAL,
	`fine`	REAL,
	`est`	REAL,
	`nord`	REAL,
	`he`	REAL,
	`hp`	REAL,
	`co`	REAL,
	`tipo`	TEXT,
	`g_med`	REAL,
	`g_stddev`	REAL,
	`sigma_ci_avg`	REAL,
	`sigma_ci_stdev`	REAL,
	`mi_med`	REAL,
	`mi_stdev`	REAL,
	`ei_med`	REAL,
	`ei_stdev`	REAL,
	`cai_med`	REAL,
	`cai_stdev`	REAL,
	`gsi_med`	REAL,
	`gsi_stdev`	REAL,
	`profilo_id`	INTEGER,
	`geoitem_id`	INTEGER,
	`rmr_med`	REAL,
	`rmr_stdev`	REAL,
	`title`	TEXT,
	`sigma_ti_min`	REAL,
	`sigma_ti_max`	REAL,
	`k0_min`	REAL,
	`k0_max`	REAL,
	`wdepth`	REAL,
	`perc`	REAL,
	`anidrite`	REAL
);
CREATE TABLE "BbtGeoitem" (
	`keyp`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`inizio`	REAL,
	`fine`	REAL,
	`l`	REAL,
	`perc`	REAL,
	`type`	TEXT,
	`g_med`	REAL,
	`g_stddev`	REAL,
	`sigma_ci_avg`	REAL,
	`sigma_ci_stdev`	REAL,
	`mi_med`	REAL,
	`mi_stdev`	REAL,
	`ei_med`	REAL,
	`ei_stdev`	REAL,
	`cai_med`	REAL,
	`cai_stdev`	REAL,
	`gsi_med`	REAL,
	`gsi_stdev`	TEXT,
	`id`	INTEGER,
	`rmr_med`	REAL,
	`rmr_stdev`	REAL,
	`title`	TEXT,
	`sigma_ti_min`	REAL,
	`sigma_ti_max`	REAL,
	`k0_min`	REAL,
	`k0_max`	REAL,
	`anidrite`	REAL
);

CREATE INDEX BbtTbmKpi_TunnelName ON BbtTbmKpi (tunnelName);
CREATE INDEX BbtTbmKpi_TbmName ON BbtTbmKpi (tbmName);
CREATE INDEX BbtTbmKpi_KpiKey ON BbtTbmKpi (kpiKey);
CREATE INDEX BbtParameterEval_TunnelName ON BbtParameterEval (tunnelName);
CREATE INDEX BbtParameterEval_TbmName ON BbtParameterEval (tbmName);
CREATE INDEX BbtParameterEval_ProfiloId ON BbtParameterEval (profilo_id);
CREATE INDEX BbtParameterEval_tunneltbm on bbtparametereval (tunnelname, tbmname);
CREATE INDEX BbtParameterEval_tunneliteration on bbtparametereval (iteration_no, tunnelname);

PRAGMA page_size = 4096;
PRAGMA locking_mode=EXCLUSIVE;
PRAGMA synchronous=NORMAL;
PRAGMA journal_mode=WAL;
PRAGMA cache_size=5000;
PRAGMA temp_store = MEMORY;
COMMIT;
