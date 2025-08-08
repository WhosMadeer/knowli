export interface TasksType {
	id: string;
	name: string;
	description?: string;
	dueDate: Date;
	status: StatusType;
	link?: string;
	weight: number;
	uid: string;
}

type StatusType = "Not Started" | "In Progress" | "Completed";
