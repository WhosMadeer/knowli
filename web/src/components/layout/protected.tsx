import { onAuthStateChanged } from "firebase/auth";
import { auth } from "@/firebase/firebase";
import { Outlet, useNavigate } from "react-router";

export function ProtectedRoute() {
	const navigate = useNavigate();

	onAuthStateChanged(auth, (user) => {
		if (user) {
			// User is signed in, see docs for a list of available properties
			// https://firebase.google.com/docs/reference/js/auth.user
			const uid = user.uid;

			console.log(uid);
		} else {
			// User is signed out

			console.error("user is signed out");
			navigate("/sign-in", { replace: true });
		}
	});

	return <Outlet />;
}
