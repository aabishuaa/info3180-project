// src/auth.js
import { reactive } from "vue";

export const auth = reactive({
  isAuthenticated: !!localStorage.getItem("token"),
  userId: localStorage.getItem("user_id")
});
