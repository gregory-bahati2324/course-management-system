import { HomeIcon, BookOpen, Users, MessageSquare, Award, BarChart3, Settings, Calendar, FileText, Plus, Eye, Edit } from "lucide-react";
import Index from "./pages/Index.tsx";
import Home from "./pages/Home.tsx";
import Dashboard from "./pages/Dashboard.tsx";
import InstructorDashboard from "./pages/instructor/Dashboard.tsx";
import CreateCourse from "./pages/instructor/CreateCourse.tsx";
import InstructorSchedule from "./pages/instructor/Schedule.tsx";
import CourseManage from "./pages/instructor/CourseManage.tsx";
import StudentReview from "./pages/instructor/StudentReview.tsx";
import MessageStudents from "./pages/instructor/MessageStudents.tsx";
import InstructorAnalytics from "./pages/instructor/Analytics.tsx";
import ScheduleSession from "./pages/instructor/ScheduleSession.tsx";
import EditCourseDescription from "./pages/instructor/EditCourseDescription.tsx";
import AddModule from "./pages/instructor/AddModule.tsx";
import CreateAssignment from "./pages/instructor/CreateAssignment.tsx";
import ViewAssignment from "./pages/instructor/ViewAssignment.tsx";
import GradeAssignment from "./pages/instructor/GradeAssignment.tsx";
import AdminDashboard from "./pages/admin/Dashboard.tsx";
import Courses from "./pages/Courses.tsx";
import CourseDetail from "./pages/CourseDetail.tsx";
import Forums from "./pages/Forums.tsx";
import Certificates from "./pages/Certificates.tsx";
import Login from "./pages/auth/Login.tsx";
import Register from "./pages/auth/Register.tsx";
import NotFound from "./pages/NotFound.tsx";

export const navItems = [
  {
    title: "Home",
    to: "/",
    icon: <HomeIcon className="h-4 w-4" />,
    page: <Index />,
  },
  {
    title: "Welcome",
    to: "/home",
    icon: <HomeIcon className="h-4 w-4" />,
    page: <Home />,
  },
  {
    title: "Student Dashboard",
    to: "/dashboard",
    icon: <BarChart3 className="h-4 w-4" />,
    page: <Dashboard />,
  },
  {
    title: "Instructor Dashboard", 
    to: "/instructor/dashboard",
    icon: <BarChart3 className="h-4 w-4" />,
    page: <InstructorDashboard />,
  },
  {
    title: "Create Course",
    to: "/instructor/create-course",
    icon: <BookOpen className="h-4 w-4" />,
    page: <CreateCourse />,
  },
  {
    title: "Instructor Schedule",
    to: "/instructor/schedule",
    icon: <BarChart3 className="h-4 w-4" />,
    page: <InstructorSchedule />,
  },
  {
    title: "Course Management",
    to: "/instructor/course/:id/manage",
    icon: <BookOpen className="h-4 w-4" />,
    page: <CourseManage />,
  },
  {
    title: "Student Review",
    to: "/instructor/review",
    icon: <Users className="h-4 w-4" />,
    page: <StudentReview />,
  },
  {
    title: "Message Students",
    to: "/instructor/messages",
    icon: <MessageSquare className="h-4 w-4" />,
    page: <MessageStudents />,
  },
  {
    title: "Instructor Analytics",
    to: "/instructor/analytics",
    icon: <BarChart3 className="h-4 w-4" />,
    page: <InstructorAnalytics />,
  },
  {
    title: "Schedule Session",
    to: "/instructor/schedule-session",
    icon: <Calendar className="h-4 w-4" />,
    page: <ScheduleSession />,
  },
  {
    title: "Edit Course Description",
    to: "/instructor/course/:id/edit-description",
    icon: <FileText className="h-4 w-4" />,
    page: <EditCourseDescription />,
  },
  {
    title: "Add Module",
    to: "/instructor/course/:id/add-module",
    icon: <Plus className="h-4 w-4" />,
    page: <AddModule />,
  },
  {
    title: "Create Assignment",
    to: "/instructor/course/:id/create-assignment",
    icon: <FileText className="h-4 w-4" />,
    page: <CreateAssignment />,
  },
  {
    title: "View Assignment",
    to: "/instructor/course/:id/assignment/:assignmentId/view",
    icon: <Eye className="h-4 w-4" />,
    page: <ViewAssignment />,
  },
  {
    title: "Grade Assignment",
    to: "/instructor/course/:id/assignment/:assignmentId/submission/:submissionId/grade",
    icon: <Edit className="h-4 w-4" />,
    page: <GradeAssignment />,
  },
  {
    title: "Admin Dashboard",
    to: "/admin/dashboard", 
    icon: <Settings className="h-4 w-4" />,
    page: <AdminDashboard />,
  },
  {
    title: "Courses",
    to: "/courses",
    icon: <BookOpen className="h-4 w-4" />,
    page: <Courses />,
  },
  {
    title: "Course Detail",
    to: "/course/:id",
    icon: <BookOpen className="h-4 w-4" />,
    page: <CourseDetail />,
  },
  {
    title: "Forums",
    to: "/forums",
    icon: <MessageSquare className="h-4 w-4" />,
    page: <Forums />,
  },
  {
    title: "Certificates",
    to: "/certificates",
    icon: <Award className="h-4 w-4" />,
    page: <Certificates />,
  },
  {
    title: "Login",
    to: "/auth/login",
    icon: <Users className="h-4 w-4" />,
    page: <Login />,
  },
  {
    title: "Register", 
    to: "/auth/register",
    icon: <Users className="h-4 w-4" />,
    page: <Register />,
  },
  {
    title: "Not Found",
    to: "*",
    icon: <HomeIcon className="h-4 w-4" />,
    page: <NotFound />,
  },
];