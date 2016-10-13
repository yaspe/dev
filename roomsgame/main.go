package main

import (
	"math/rand"
	"roomsgame/core"
	"time"
)

func main() {
	rand.Seed(time.Now().UTC().UnixNano())

	var house = core.NewHouse()

	var rooms = house.GetRooms()
	for y := range rooms {
		for x := range rooms[y] {
			room_type := rooms[y][x].GetType()
			if room_type == core.RT_PASSAGE {
				print(" ")
			} else if room_type == core.RT_ENTRANCE {
				print("^")
			} else {
				print("X")
			}
		}
		println()
	}
}
