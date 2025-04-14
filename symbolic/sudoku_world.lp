% rules
% cell(X, Y, V)
value(1..9).
pos(1..9).
group(1..9).

% group
group(X, Y, 1) :- cell(X, Y, _), X <= 3, Y <= 3.
group(X, Y, 2) :- cell(X, Y, _), X <= 3, 3 < Y <= 6.
group(X, Y, 3) :- cell(X, Y, _), X <= 3, 6 < Y <= 9.
group(X, Y, 4) :- cell(X, Y, _), 3 < X <= 6, Y <= 3.
group(X, Y, 5) :- cell(X, Y, _), 3 < X <= 6, 3 < Y <= 6.
group(X, Y, 6) :- cell(X, Y, _), 3 < X <= 6, 6 < Y <= 9.
group(X, Y, 7) :- cell(X, Y, _), 6 < X <= 9, Y <= 3.
group(X, Y, 8) :- cell(X, Y, _), 6 < X <= 9, 3 < Y <= 6.
group(X, Y, 9) :- cell(X, Y, _), 6 < X <= 9, 6 < Y <= 9.

% rows and columns cannot have the same value
:- cell(X, Y, V), cell(X2, Y, V2), X != X2, not V != V2.
:- cell(X, Y, V), cell(X, Y2, V2), Y != Y2, not V != V2.
% group cannot have the same value
:- cell(X, Y, V), cell(X2, Y2, V2), group(X, Y, G), group(X2, Y2, G), X != X2, Y != Y2, not V != V2.
:- cell(X, Y, V), cell(X, Y, V2), not V == V2.
