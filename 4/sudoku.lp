
sudoku(X,Y,N) :- initial(X,Y,N).

1 { sudoku(1..9,Y,N) } 1 :- Y=1..9, N=1..9.
1 { sudoku(X,1..9,N) } 1 :- X=1..9, N=1..9.
1 { sudoku(X,Y,1..9) } 1 :- X=1..9, Y=1..9.

:- sudoku(X1,Y1,N), sudoku(X2,Y2,N), (X1,Y1) != (X2,Y2), (((X1-1)/3),((Y1-1)/3)) == (((X2-1)/3), ((Y2-1)/3)).


#show sudoku/3.
