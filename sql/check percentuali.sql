select title, (max(fine)-min(fine))/10+1  from bbtparametereval
where tbmname = 'XXX'
and perc = 0.01
group by title


select title, count(*)/3 from BbtParameterEval
where tunnelname != 'XXX'
and tbmname = 'GL_DS_HRK_10.60_00'
and title in (
select distinct title  from bbtparametereval
where tbmname = 'XXX'
and perc = 0.01)
group by title