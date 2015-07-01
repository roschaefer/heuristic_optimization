CXX = g++
CXXFLAGS = -Wall 
OPTFLAGS = -O2
INCLUDES = -I$(PWD)

SOURCES = Evaluator.cc 
OBJECTS = $(SOURCES:.cc=.o)
BIN = fcost

main: $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(BIN) $(OBJECTS) main.cc $(INCLUDES) $(OPTFLAGS)

.cpp.o:
	$(CC) $(CFLAGS) -c $< -o $@ -w $(INCLUDES) $(OPTFLAGS)

clean:
	-rm -f $(OBJECTS) $(BIN) 2> /dev/null
