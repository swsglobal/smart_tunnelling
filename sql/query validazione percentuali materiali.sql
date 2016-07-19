select BbtParameterEval.tunnelname, BbtParameterEval.tbmname, BbtParameterEval.fine, BbtParameterEval.title, count(BbtParameterEval.title)/300.0, bbtparameter.perc
from BbtParameterEval inner join bbtparameter on BbtParameterEval.fine = bbtparameter.fine and BbtParameterEval.title = bbtparameter.title
where tunnelname = "GL Nord"
group by BbtParameterEval.tunnelname, BbtParameterEval.tbmname, BbtParameterEval.fine, BbtParameterEval.title