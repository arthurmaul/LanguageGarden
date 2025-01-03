package main

import (
    "fmt"
    "strings"
)

type queue [T any] struct {
    buffer []T
}

func Queue[T any](values ...T) *queue[T] {
    return &queue[T]{values}
}

func (q *queue[T]) String() string {
    strs := []string{}
    for _, element := range q.buffer {
        strs = append(strs, fmt.Sprint(element))
    }
    return "queue(" + strings.Join(strs, ", ") + ")"
}

func (q *queue[T]) push(element T) *queue[T] {
    q.buffer = append(q.buffer, element)
    return q
}

func (q *queue[T]) pushLeft(element T) *queue[T] {
    q.buffer = append([]T{element}, q.buffer...)
	return q
}

func (q *queue[T]) pullLeft() T {
    value := q.buffer[0]
    q.buffer = q.buffer[1:]
    return value
}

func (q *queue[T]) empty() bool {
    return len(q.buffer) > 0
}

func main() {
    q := Queue(9128, 1, 2, 3)
    fmt.Println(q.pullLeft())
    q.pushLeft(0)
    q.push(4)
    fmt.Println(q)
}
