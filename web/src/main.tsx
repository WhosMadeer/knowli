import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import { Upload } from "./app/file-upload/upload";
import App from "./App";
import Calendar from "./app/calendar";
import "./index.css";
import { SignUpPage } from "./app/auth/sign-up";
import { ProtectedRoute } from "./components/layout/protected";
import { SignInPage } from "./app/auth/sign-in";

createRoot(document.getElementById("root")!).render(
	<StrictMode>
		<BrowserRouter>
			<Routes>
				<Route element={<ProtectedRoute />}>
					<Route index element={<Upload />} />
					<Route path="/app" element={<App />} />
					<Route path="/cal" element={<Calendar />} />
				</Route>
				<Route path="/sign-up" element={<SignUpPage />} />
				<Route path="/sign-in" element={<SignInPage />} />
			</Routes>
		</BrowserRouter>
	</StrictMode>
);
