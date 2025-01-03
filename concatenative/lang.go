package main

import (
    "fmt"
    "errors"
)

type Parser func(string) (error)

func symbol(expected string) Parser {
	return func(text string) (error) {
    	if string(text[0]) == expected {
        	return nil
    	}
    	return errors.New("Expected rune was not found")
	}
}

type program struct {
    source string
    queue []string
    done bool
    line int
    position int
    cursor int
}

func Program(source string) *program {
	return &program{source, []string{}, false, 1, 1, 0}
}

func (p *program) nl() {
    p.cursor++
	p.line++
	p.position = 0
}

func (p *program) progress() {
    p.cursor++
    p.position++
}

func (p *program) read() string {
    whitespace := symbol(" ")
    var lexeme string
    processing:
	for !p.done {
    	if p.cursor == len(p.source) {
        	if lexeme != "" {
            	return lexeme
        	}
			p.done = true
			return "EOF"
    	}
        current := string(p.source[p.cursor])
    	err := whitespace(current)
    	if err == nil {
        	p.progress()
        	break processing
        } else if current == "\n" {
            p.nl()
        } else {
        	lexeme += current
        	p.progress()
    	}
	}
	return lexeme
}

func main() {
	p := Program("hello world wahooooo yippeeeee itsa mea mario !")
	fmt.Println(p.read())
	fmt.Println(p.read())
	fmt.Println(p.read())
	fmt.Println(p.read())
	fmt.Println(p.read())
	fmt.Println(p.read())
	fmt.Println(p.read())
	fmt.Println(p.read())
	fmt.Println(p.read())
}
