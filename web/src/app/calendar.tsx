import { Calendar } from "@/components/ui/calendar"
import React from "react";

function CalendarPage() {
    const today = new Date(); 
    const day = today.getDate();
    const week = today.getDay();

    const DaysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']; 
    const [date, setDate] = React.useState<Date | undefined>(new Date())

return (
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
                <div className="w-screen h-10 border-2">
    
                </div>
                {Array.from({ length: 24 }, (_, i) => i + 1).map((hour) => {
                    return (
                        <div className=" text-black border-2 w-20 my-2 p-4">
                            {hour}
                            {hour > 12 ? 'PM' : 'AM'}
                        </div>
                    );
                })}
            </div>
        </div>
        </div>
    )


}

export default CalendarPage; 