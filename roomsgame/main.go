package main

import (
	"fmt"
	"math/rand"
	"roomsgame/core"
	"time"
)

func main() {
	rand.Seed(time.Now().UTC().UnixNano())

	var house = core.NewHouse()

	fmt.Println("")

	var rooms = house.GetRooms()
	for y := range rooms {
		for x := range rooms[y] {
			room_type := rooms[y][x].GetType()
			if room_type == 0 {
				fmt.Print(" ")
			} else if room_type == 1 {
				fmt.Print("^")
			} else {
				fmt.Print("X")
			}
		}
		fmt.Println("")
	}
}
