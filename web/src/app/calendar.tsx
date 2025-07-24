import { Calendar } from "@/components/ui/calendar"
import React from "react";
import *

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"



function CalendarPage() {
    const today = new Date(); 
    const day = today.getDate();
    const week = today.getDay();

    const DaysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']; 
    const [date, setDate] = React.useState<Date | undefined>(new Date())

return (
    <>
    <Select>
        <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Select a fruit" />
        </SelectTrigger>
        <SelectContent>
            <SelectGroup>
                <SelectLabel>Fruits</SelectLabel>
                <SelectItem value="apple">Apple</SelectItem>
                <SelectItem value="banana">Banana</SelectItem>
                <SelectItem value="blueberry">Blueberry</SelectItem>
                <SelectItem value="grapes">Grapes</SelectItem>
                <SelectItem value="pineapple">Pineapple</SelectItem>
            </SelectGroup>
        </SelectContent>
    </Select>
    
    <div className="flex items-start gap-4 p-4">

            <Calendar
                mode="single"
                selected={date}
                onSelect={setDate}
                className="rounded-lg border" /><div>

                <div className="text-lg font-semibold">
                    <h1>{DaysOfWeek[week]}, {day}</h1>
                </div>
                <div className=" border-2 p-2 w-screen">
                    {Array.from({ length: 24 }, (_, i) => i + 1).map((hour) => {
                        return (
                            <div className="flex gap-2">
                                <div className=" text-black border-white border-2 w-21 p-4">
                                    {hour}
                                    {hour > 12 ? 'PM' : 'AM'}
                                </div>
                                <div className="w-screen h-14 border-2"></div>

                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
        </>

        
    )


}



export default CalendarPage; 