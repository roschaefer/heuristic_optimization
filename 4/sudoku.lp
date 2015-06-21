


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% problem instance
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% first row
%
initial(2,2,10).
initial(3,3,15).
%
initial(6,2,11).
initial(7,2,15).
initial(6,3,10).
initial(7,3,3).
%
initial(10,2,3).
initial(11,2,14).
initial(10,3,8).
initial(11,3,2).
%
initial(14,2,8).
initial(16,1,5).
initial(16,2,7).
initial(16,3,6).
initial(16,4,15).


%
% second row
%
initial(2,6,5).
initial(3,6,12).
initial(2,7,15).
initial(3,7,11).
%
initial(6,6,9).
initial(7,7,5).
%
initial(11,5,11).
initial(9,8,7).
initial(10,8,5).
initial(11,8,8).
initial(12,8,6).
%
initial(14,6,2).
initial(15,6,7).
initial(14,7,14).
initial(15,7,4).
%


%
% third row
%
initial(1,12,14).
initial(2,12,6).
initial(3,12,13).
initial(4,12,3).
%
initial(5,9,14).
initial(6,9,4).
initial(5,10,2).
initial(6,10,15).
%
initial(10,10,9).
initial(11,11,6).
%
initial(13,12,15).
initial(14,12,5).
initial(15,12,16).
initial(16,12,4).


%
% fourth row
%
initial(4,13,10).
initial(4,14,7).
initial(4,15,13).
initial(4,16,1).
%
initial(5,14,1).
initial(6,14,12).
initial(7,14,2).
initial(8,14,10).
%
initial(9,13,3).
initial(9,14,8).
initial(9,15,15).
initial(9,16,6).
%
initial(14,14,15).
initial(15,15,12).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% problem encoding
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sudoku(X,Y,N) :- initial(X,Y,N).

1 { sudoku(1..9,Y,N) } 1 :- Y=1..9, N=1..9.
1 { sudoku(X,1..9,N) } 1 :- X=1..9, N=1..9.
1 { sudoku(X,Y,1..9) } 1 :- X=1..9, Y=1..9.

:- sudoku(X1,Y1,N), sudoku(X2,Y2,N), (X1,Y1) != (X2,Y2), (((X1-1)/3),((Y1-1)/3)) == (((X2-1)/3), ((Y2-1)/3)).


#show sudoku/3.
