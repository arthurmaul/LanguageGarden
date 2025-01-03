package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
)

type Sibu struct {
    stopped bool
    queue []string
    images []Image
    lexicon map[string][]string
}

type Image struct {
    source string
    queue []string
	finished bool
	failed bool
	line int
	position int
	cursor int
}

func (image Image) read() string {
	var lexeme []string
	fmt.Println(lexeme)
	reading:
	for !image.finished {
		break reading
	}
	return ""
}

func main() {
    reader := bufio.NewReader(os.Stdin)
    fmt.Println("S i b u")

	dialog:
	for {
        fmt.Print("() :: \n")
        text, _ := reader.ReadString(';')
        text = strings.Replace(text, ";", "", -1)
        fmt.Println(text)
        if text[len(text)-3:len(text)] == "bye" {
            break dialog
        }
	}
}

