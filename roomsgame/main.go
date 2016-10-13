package main

import (
	"math/rand"
	"roomsgame/core"
	"time"
)

func draw(house core.IHouse) {
	var rooms = house.GetRooms()
	for i := range rooms {
		for j := range rooms[i] {
			ii, jj := house.GetPlayerPos()
			if uint(i) == ii && uint(j) == jj {
				print("*")
				continue
			}
			room_type := rooms[i][j].GetType()
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

func main() {
	rand.Seed(time.Now().UTC().UnixNano())

	house := core.NewHouse()
	draw(house)
}
