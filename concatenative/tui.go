package main

import (
	"fmt"
	"strings"
)

type AnsiFormat int

// General styling
const (
	Normal AnsiFormat = iota
	Bold
	Faint
	Italic
	Underline
	Blink
	FastBlink
	Inverse
	Hidden
	Strikeout
)

type AnsiColor int

// 8 standard colors
const (
	Black AnsiColor = iota + 30
	Red
	Green
	Yellow
	Blue
	Magenta
	Cyan
	White
)

// 8 bright colors
const (
	BrightBlack AnsiColor = iota + 90
	BrightRed
	BrightGreen
	BrightYellow
	BrightBlue
	BrightMagenta
	BrightCyan
	BrightWhite
)

type style struct {
	settings   []AnsiFormat
	foreground AnsiColor
	background AnsiColor
}

func Style() *style {
	s := style{settings: []AnsiFormat{}, foreground: White, background: Black}
	return &s
}

func (s *style) Painted(setting AnsiColor) *style {
	s.foreground = setting
	return s
}

func (s *style) On(setting AnsiColor) *style {
	s.background = setting + 10
	return s
}

func (s *style) With(settings ...AnsiFormat) *style {
	for _, setting := range settings {
		s.settings = append(s.settings, setting)
	}
	return s
}

func (s *style) String() string {
	return set(s.settings...) + set(s.foreground, s.background)
}

func (s *style) Format(text string) string {
    return s.String() + text + set(Normal)
}

func (s *style) Print(text string) {
    fmt.Print(s.Format(text))
}

func (s *style) Println(text string) {
    fmt.Println(s.Format(text))
}

func set[AnsiSetting AnsiColor | AnsiFormat](settings ...AnsiSetting) string {
	strs := []string{}
	for _, setting := range settings {
		strs = append(strs, fmt.Sprint(setting))
	}
	return "\033[" + strings.Join(strs, ";") + "m"
}

func main() {
	s := Style().Painted(BrightWhite).On(Black).With(Bold, Italic)
	s.Println("hello world")
}
