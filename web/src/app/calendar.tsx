import { Calendar } from "@/components/ui/calendar"
import React, { useState } from "react";

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"


const items = [
  {
    id: "recents",
    label: "Recents",
  },
  {
    id: "home",
    label: "Home",
  },
  {
    id: "applications",
    label: "Applications",
  },
  {
    id: "desktop",
    label: "Desktop",
  },
  {
    id: "downloads",
    label: "Downloads",
  },
  {
    id: "documents",
    label: "Documents",
  },
] as const

const FormSchema = z.object({
  items: z.array(z.string()).refine((value) => value.some((item) => item), {
    message: "You have to select at least one item.",
  }),
})

function CalendarCheckbox() {
  const [toggle, setToggle] = useState(false);

  return (
    <div>
        <Checkbox checked={toggle} onCheckedChange={() => setToggle((curr) => !curr)}/>
    </div>
  )
} 




function CalendarPage() {
    const today = new Date(); 
    const day = today.getDate();
    const week = today.getDay();

    const DaysOfWeek = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']; 
    const [date, setDate] = React.useState<Date | undefined>(new Date())

    const [view, setView] = useState("")

return (
    <>
    <div className="pl-4 pt-4">
    <Select value={view} onValueChange={(value) => setView(value)}>
        <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Select a layout"/>
        </SelectTrigger>
        <SelectContent>
            <SelectGroup>
                <SelectItem value="Day">Day</SelectItem>
                <SelectItem value="Week">Week</SelectItem>
                <SelectItem value="Month">Month</SelectItem>
                <SelectItem value="Year">Year</SelectItem>
            </SelectGroup>
        </SelectContent>
    </Select></div>

    
    <div className="flex items-start gap-4 p-4">

            <Calendar
                mode="single"
                selected={date}
                onSelect={setDate}
                className="rounded-lg border" /><div>

                <div className="-mt-15">

                  {view === "Day" && (
                    <div className=" font-semibold text-xl p-2">
                    <h1>{DaysOfWeek[week]}, {day}</h1>
                    </div>
                  )}


                <div className="">
                  <h1>My Subjects</h1>
                </div>


                <div className=" border-2 p-2 w-screen border-white">
                    {view === "Day" && Array.from({ length: 24 }, (_, i) => i + 1).map((hour) => {
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
                    {view === "Week" && <WeekPage date={date} setDate={setDate}/>}
                    {view === "Month" && <MonthPage date={date} setDate={setDate}/>}
                </div>
                </div>
            </div>
        </div>
        </>

        
    )


}


function WeekPage ({date, setDate}: {date: Date | undefined, setDate: React.Dispatch<React.SetStateAction<Date | undefined>>}) {

    const today = new Date(); 
    const DaysOfWeek = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];

    return (
    <>  

                <div className="flex flex-row gap-2 font-semibold text-xl p-2">
                {date && Array.from({ length: 7}, (_, i) => i).map((i) => {
                    date.setDate(date.getDate() + i); 

                    return (
                        <div className="border-2 p-4 ml-20 h-400 w-40 text-center">
                        {DaysOfWeek[date.getDay()]} {date.getDate()}
                        </div>
                    ); 
                })}
                </div>

                <div className="-mt-370 -ml-1">
                    {Array.from({ length: 24 }, (_, i) => i + 1).map((hour) => {
                        return (
                            <div className="flex gap-2">
                                <div className=" text-black border-white border-2 w-21 p-2">
                                    {hour}
                                    {hour > 12 ? 'PM' : 'AM'}
                                </div>
                                <div className="w-412 h-14 border-2"></div>

                            </div>
                        );
                    })}
                </div>
        </>

    )
        
}



function MonthPage({date, setDate}: {date: Date | undefined, setDate: React.Dispatch<React.SetStateAction<Date | undefined>>}) {

  if (date === undefined) {
    return <div>No date</div>
  }

  const today = new Date();
  const month = date.getMonth(); 
  const year = date.getFullYear();   


    const DaysOfWeek = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
    const daysInMonths = [31, (year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0)) 
    ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

    const daysInMonth = daysInMonths[month];
    

      return (

                <>
                <div className="flex flex-row gap-2 font-semibold text-xl p-2">
                {date && Array.from({ length: 7 }, (_, i) => i).map((i) => {
              date.setDate(date.getDate() + i);

            return (
              <div className="border-2 p-4 ml-20 h-400 w-40 text-center">
                {DaysOfWeek[date.getDay()]} {date.getDate()}
              </div>
            );
          })}
            </div>
        
        <div className="">
            {Array.from({ length: daysInMonth }, (_, i) => i + 1).map((i) => {
              return (
                <div className="border-1">
                  {i}
                </div>
              );
            })}
          </div>
          </>
      )
}

export default CalendarPage; 