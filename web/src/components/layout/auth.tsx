import type { PropsWithChildren } from "react";

export default function AuthLayout({ children }: PropsWithChildren) {
	return <div className="min-h-svh w-screen flex flex-col bg-background items-center justify-center">{children}</div>;
}
