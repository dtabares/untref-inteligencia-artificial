%Hechos
count([], 0).
%Reglas
count([H|T], N):-count(T, N1),N is N1+1.