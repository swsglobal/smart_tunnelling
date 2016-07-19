/* trova le sigma v e h maggiori e minori e le sigma h e v rispettive per lo scudo anteriore*/
SELECT a.tunnelname, a.tbmname, a.fine, a.title, a.sigma_v_max_front_shield, a.sigma_h_max_front_shield
FROM bbtparametereval a
INNER JOIN (
    SELECT tunnelname, tbmname, min(sigma_v_max_front_shield) min_sigma_v, max(sigma_v_max_front_shield) max_sigma_v, min(sigma_h_max_front_shield) min_sigma_h, max(sigma_h_max_front_shield) max_sigma_h
    FROM bbtparametereval
	where tunnelname != 'XXX' and sigma_v_max_front_shield > 0
    GROUP BY tunnelname, tbmname
) b 
ON a.tunnelname = b.tunnelname AND a.tbmname = b.tbmname AND (
a.sigma_v_max_front_shield = b.min_sigma_v OR a.sigma_v_max_front_shield = b.max_sigma_v 
OR a.sigma_h_max_front_shield = b.min_sigma_h OR a.sigma_h_max_front_shield = b.max_sigma_h)
order by a.tunnelname, a.tbmname, a.sigma_v_max_front_shield, a.sigma_h_max_front_shield

/* trova le sigma v e h maggiori e minori e le sigma h e v rispettive per lo scudo posteriore*/
SELECT a.tunnelname, a.tbmname, a.fine, a.title, a.sigma_v_max_tail_skin, a.sigma_h_max_tail_skin
FROM bbtparametereval a
INNER JOIN (
    SELECT tunnelname, tbmname, min(sigma_v_max_tail_skin) min_sigma_v, max(sigma_v_max_tail_skin) max_sigma_v, min(sigma_h_max_tail_skin) min_sigma_h, max(sigma_h_max_tail_skin) max_sigma_h
    FROM bbtparametereval
	where tunnelname != 'XXX' and sigma_v_max_tail_skin > 0
    GROUP BY tunnelname, tbmname
) b 
ON a.tunnelname = b.tunnelname AND a.tbmname = b.tbmname AND (
a.sigma_v_max_tail_skin = b.min_sigma_v OR a.sigma_v_max_tail_skin = b.max_sigma_v 
OR a.sigma_h_max_tail_skin = b.min_sigma_h OR a.sigma_h_max_tail_skin = b.max_sigma_h)
order by a.tunnelname, a.tbmname, a.sigma_v_max_tail_skin, a.sigma_h_max_tail_skin

/* trova le sigma v e h maggiori e minori e le sigma h e v rispettive per l'anello*/
SELECT a.tunnelname, a.tbmname, a.fine, a.title, a.sigma_v_max_lining, a.sigma_h_max_lining
FROM bbtparametereval a
INNER JOIN (
    SELECT tunnelname, tbmname, min(sigma_v_max_lining) min_sigma_v, max(sigma_v_max_lining) max_sigma_v, min(sigma_h_max_lining) min_sigma_h, max(sigma_h_max_lining) max_sigma_h
    FROM bbtparametereval
	where tunnelname != 'XXX' and sigma_v_max_lining > 0
    GROUP BY tunnelname, tbmname
) b 
ON a.tunnelname = b.tunnelname AND a.tbmname = b.tbmname AND (
a.sigma_v_max_lining = b.min_sigma_v OR a.sigma_v_max_lining = b.max_sigma_v 
OR a.sigma_h_max_lining = b.min_sigma_h OR a.sigma_h_max_lining = b.max_sigma_h)
order by a.tunnelname, a.tbmname, a.sigma_v_max_lining, a.sigma_h_max_lining



/* funzione generale per python che accetta 2 parametri in ingresso correlati tra loro*/
SELECT a.tunnelname, a.tbmname, a.fine, a.title, a.sigma_v_max_{0}, a.sigma_h_max{1}
FROM bbtparametereval a
INNER JOIN (
    SELECT tunnelname, tbmname, min(sigma_v_max_{0}) min_par1, max(sigma_v_max_{0}) max_par1, min(sigma_h_max_{0}) min_par2, max(sigma_h_max_{0}) max_par2
    FROM bbtparametereval
	where tunnelname != 'XXX' and sigma_v_max_{0} > 0 and sigma_h_max_{0} > 0
    GROUP BY tunnelname, tbmname
) b 
ON a.tunnelname = b.tunnelname AND a.tbmname = b.tbmname AND (
a.sigma_v_max_{0} = b.min_par1 OR a.sigma_v_max_{0} = b.max_par1 
OR a.and sigma_h_max_{0} = b.min_par2 OR a.and sigma_h_max_{0} = b.max_par2)
order by a.tunnelname, a.tbmname, a.sigma_v_max_{0}, a.and sigma_h_max_{0}


select tunnelname, tbmname, count(fine)* 10
From(
	SELECT tunnelname, tbmname, fine, count(overcut_required)
	FROM bbtparametereval
	where overcut_required > 0
	group by tunnelname, tbmname, fine)
group by tunnelname, tbmname
order by tunnelname, tbmname

select tunnelname, tbmname, count(fine)* 10
From(
	SELECT tunnelname, tbmname, fine, count(auxiliary_thrust_required)
	FROM bbtparametereval
	where auxiliary_thrust_required > 0
	group by tunnelname, tbmname, fine)
group by tunnelname, tbmname
order by tunnelname, tbmname

select tunnelname, tbmname, count(fine)* 10
From(
	SELECT tunnelname, tbmname, fine, count(consolidation_required)
	FROM bbtparametereval
	where consolidation_required > 0
	group by tunnelname, tbmname, fine)
group by tunnelname, tbmname
order by tunnelname, tbmname

select tunnelname, tbmname, count(fine)* 10
From(
	SELECT tunnelname, tbmname, fine, count({0})
	FROM bbtparametereval
	where {0} > 0
	group by tunnelname, tbmname, fine)
group by tunnelname, tbmname
order by tunnelname, tbmname

/*tabella con riassunto tunnel, tbm e probabilità occorrenza */
select * from(
SELECT tunnelname, tbmname, fine, CAST(sum({0}) AS REAL)/cast(count({0}) as real) as probability
FROM bbtparametereval
group by tunnelname, tbmname, fine
order by tunnelname, tbmname
) where probability > 0

/* per singolo tunnel*/
select * from(
SELECT fine, CAST(sum({0}) AS REAL)/cast(count({0}) as real) as probability
FROM bbtparametereval
where tunnelname = '{1}' AND tbmname = '{2}'
group by fine
order by fine
) where probability > 0
