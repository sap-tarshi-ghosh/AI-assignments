%1.rule to assign grade based on marks

grade(Marks, 'A') :- Marks >= 80.
grade(Marks, 'B') :- Marks >= 60, Marks < 80.
grade(Marks, 'C') :- Marks >= 40, Marks < 60.
grade(Marks, 'F') :- Marks < 40.

%2.formula: F = (C * 9/5) + 32
convert(C, F) :-
    F is (C * 9/5) + 32.

%3.calculate factorial of a number
%base case
factorial(0, 1).

%recursive case
factorial(N, F) :-
    N > 0,
    N1 is N - 1,
    factorial(N1, F1),
    F is N * F1.


%4.print even number in a range
print_even(L, H) :-
    L =< H,
    (   0 is L mod 2
    ->  write(L), nl
    ;   true
    ),
    L1 is L + 1,
    print_even(L1, H).

print_even(L, H) :-
    L > H.