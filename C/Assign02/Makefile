CC			=	gcc
CFLAGS		=	-Wall -Wextra -g
LDFLAGS 	= 	-lm
OBJFILES	= assign02_algo.o
TARGET		= assign02_algo

all: $(TARGET)

$(TARGET): $(OBJFILES)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJFILES) $(LDFLAGS)

clean:
	rm -f $(OBJFILES) $(TARGET) 
	rm -f test_return.txt
	rm -f output_file.txt