import z from "zod";

export const userSchema = z.object({
	// username: z.string().min(6, "Username must be greater than 6 characters"),
	email: z.email().min(1, "Email is required"),
	password: z.string().min(8, "Password must be greater than 8 characters"),
});

export type userSchemaType = z.infer<typeof userSchema>;
