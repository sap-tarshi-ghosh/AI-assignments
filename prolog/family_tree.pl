% gender
male(ram).
male(paul).
male(mike).
male(tom).

female(mary).
female(linda).
female(susan).
female(anna).

% parent relationships
parent(ram, paul).
parent(mary, paul).

parent(ram, linda).
parent(mary, linda).

parent(paul, mike).
parent(susan, mike).

parent(paul, anna).
parent(susan, anna).

parent(tom, ram).


% Father: X is father of Y if X is male and parent of Y
father(X, Y) :-
    parent(X, Y),
    male(X).

% Mother: X is mother of Y if X is female and parent of Y
mother(X, Y) :-
    parent(X, Y),
    female(X).

% Sister: X is sister of Y if
% X is female, they share at least one parent, and X ≠ Y
sister(X, Y) :-
    parent(P, X),
    parent(P, Y),
    female(X),
    X \= Y.

% Grandfather: X is grandfather of Y if
% X is male and parent of a parent of Y
grandfather(X, Y) :-
    parent(X, Z),
    parent(Z, Y),
    male(X).