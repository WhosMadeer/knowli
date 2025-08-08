import AuthLayout from "@/components/layout/auth";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { auth } from "@/firebase/firebase";
import { userSchema, type userSchemaType } from "@/schemas/user";
import { zodResolver } from "@hookform/resolvers/zod";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router";

export function SignUpPage() {
	return (
		<AuthLayout>
			<div className="grid gap-4">
				<div className="flex flex-col gap-2 items-center text-center">
					<h1 className="text-lg font-bold">Welcome to Knowli.</h1>
					<span className="text-sm">
						Already have an account?{" "}
						<Link to="/sign-in" className="underline underline-offset-4">
							Sign in
						</Link>
					</span>
				</div>
				<SignUpForm />
			</div>
		</AuthLayout>
	);
}

function SignUpForm() {
	const navigate = useNavigate();

	const form = useForm<userSchemaType>({
		resolver: zodResolver(userSchema),
		defaultValues: {
			email: "",
			password: "",
		},
	});

	const onSubmit = async (data: userSchemaType) => {
		try {
			console.log(data);
			const { email, password } = data;
			const userCredential = await createUserWithEmailAndPassword(auth, email, password);

			const user = userCredential.user;

			if (user) {
				navigate("/", { replace: true });
			}
		} catch (error) {
			console.error(error);
		}
	};

	return (
		<Form {...form}>
			<form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col gap-6 w-sm">
				<div className="flex flex-col gap-2 w-full">
					<FormField
						control={form.control}
						name="email"
						render={({ field }) => (
							<FormItem>
								<FormLabel>Email</FormLabel>
								<FormControl>
									<Input {...field} />
								</FormControl>
								<FormMessage />
							</FormItem>
						)}
					/>
					<FormField
						control={form.control}
						name="password"
						render={({ field }) => (
							<FormItem>
								<FormLabel>Password</FormLabel>
								<FormControl>
									<Input {...field} />
								</FormControl>
								<FormMessage />
							</FormItem>
						)}
					/>
				</div>
				<Button type="submit">Sign up</Button>
			</form>
		</Form>
	);
}
