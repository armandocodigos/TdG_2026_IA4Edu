import { RouterProvider } from "react-router";

import { AuthProvider } from "@/app/features/auth/AuthProvider";
import { router } from "@/app/routes";

export default function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
}
