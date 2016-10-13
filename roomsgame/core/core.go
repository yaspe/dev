package core

import (
	"math/rand"
)

type t_player struct {
	x, y uint
}

type RoomType int

const (
	RT_PASSAGE RoomType = iota
	RT_ENTRANCE
	RT_WALL

	RT_MAX
)

type t_room struct {
	room_type RoomType
	gen_group uint // used to generate a valid house, do not needed after generation
}

type IHouse interface {
	GetSize() uint
	GetRooms() [house_size][house_size]t_room
	GetPlayerPos() (uint, uint)
}

const house_size uint = 25

type t_house struct {
	rooms  [house_size][house_size]t_room
	player t_player
}

// methods

// house

func NewHouse() *t_house {
	house := new(t_house)

	// generation randon inner space
	for i := uint(0); i < house_size; i += 1 {
		house.rooms[0][i].room_type = RT_WALL
		house.rooms[i][0].room_type = RT_WALL
		house.rooms[house_size-1][i].room_type = RT_WALL
		house.rooms[i][house_size-1].room_type = RT_WALL
	}

	for y := uint(1); y+1 < house_size-1; y += 2 {
		for x := uint(0); 2*x < house_size; x++ {
			house.rooms[y][2*x].gen_group = x + 1
		}

		group_size := 0
		for x := uint(1); 2*(x+1) < house_size-1; x++ {
			left := &house.rooms[y][2*x]
			right := &house.rooms[y][2*x+2]
			middle := &house.rooms[y][2*x+1]
			down_left := &house.rooms[y+1][2*x]
			down_right := &house.rooms[y+1][2*x+2]
			down_middle := &house.rooms[y+1][2*x+1]

			down_left.room_type = RT_WALL
			down_right.room_type = RT_WALL
			down_middle.room_type = RT_WALL

			if left.gen_group == right.gen_group {
				continue
			}
			if rand.Intn(2) == 0 {
				right.gen_group = left.gen_group
				group_size++
			} else {
				middle.room_type = RT_WALL
				if group_size > 0 {
					house.rooms[y+1][2*(x-uint(rand.Intn(group_size)))].room_type = 0
				} else {
					down_left.room_type = 0
				}
				group_size = 0
			}
		}
		if group_size > 0 {
			house.rooms[y+1][house_size-2-2*uint(rand.Intn(group_size))].room_type = 0
		} else {
			house.rooms[y+1][house_size-2].room_type = 0
		}
	}

	house.player.x = house_size - 1
	house.player.y = house_size / 2
	house.rooms[house.player.x][house.player.y].room_type = RT_ENTRANCE
	return house
}

func (house *t_house) GetSize() uint {
	return house_size
}

func (house *t_house) GetRooms() [house_size][house_size]t_room {
	return house.rooms
}

func (house *t_house) GetPlayerPos() (uint, uint) {
	return house.player.x, house.player.y
}

// room

func (room *t_room) GetType() RoomType {
	return room.room_type
}
