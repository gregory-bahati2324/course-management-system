import { useEffect, useState } from 'react';
import { 
  BookOpen, Users, Calendar, TrendingUp, FileText, Star, Plus, Edit, Eye, MessageSquare 
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Link, useNavigate } from 'react-router-dom';
import { useToast } from '@/hooks/use-toast';

interface UserProfile {
  full_name: string;
  permission: string;
}

interface AuthMeResponse {
  id: string;
  is_active: boolean;
  profile: UserProfile;
}

export default function InstructorDashboard() {
  const { toast } = useToast();
  const navigate = useNavigate();
  const [instructor, setInstructor] = useState<AuthMeResponse | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch authentication data
  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        toast({ title: "Not Logged In", description: "Please login to continue", variant: "destructive" });
        navigate('/auth/login');
        return;
      }

      try {
        const res = await fetch('http://localhost:8000/auth/users/me', {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (!res.ok) throw new Error('Failed to fetch user info');

        const data: AuthMeResponse = await res.json();
        setInstructor(data);
      } catch (err: any) {
        toast({ title: "Error", description: err.message, variant: "destructive" });
        navigate('/auth/login');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [navigate, toast]);

  if (loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  if (!instructor) return null;

  // All other dummy data remains unchanged
  const stats = [
    { title: "Active Courses", value: "4", description: "This semester", icon: BookOpen, trend: "+1 from last semester" },
    { title: "Total Students", value: "186", description: "Across all courses", icon: Users, trend: "+23 from last semester" },
    { title: "Pending Reviews", value: "12", description: "Assignments to grade", icon: FileText, trend: "Due this week" },
    { title: "Course Rating", value: "4.8", description: "Average rating", icon: Star, trend: "Excellent feedback" }
  ];

  const courses = [
    { id: 1, title: "Advanced Database Systems", code: "CS 401", students: 45, status: "published", progress: 75, pendingSubmissions: 8, nextSession: "Dec 12, 2024 - 10:00 AM", lastActivity: "2 hours ago" },
    { id: 2, title: "Data Structures & Algorithms", code: "CS 201", students: 67, status: "published", progress: 60, pendingSubmissions: 15, nextSession: "Dec 13, 2024 - 2:00 PM", lastActivity: "1 day ago" },
    { id: 3, title: "Machine Learning Fundamentals", code: "CS 451", students: 38, status: "published", progress: 90, pendingSubmissions: 3, nextSession: "Dec 14, 2024 - 9:00 AM", lastActivity: "3 hours ago" },
    { id: 4, title: "Web Development Basics", code: "CS 301", students: 52, status: "draft", progress: 30, pendingSubmissions: 0, nextSession: "Not scheduled", lastActivity: "5 days ago" }
  ];

  const recentSubmissions = [
    { studentName: "John Mwalimu", course: "Advanced Database Systems", assignment: "Database Design Project", submittedAt: "2 hours ago", status: "pending" },
    { studentName: "Grace Kikoti", course: "Machine Learning Fundamentals", assignment: "ML Algorithm Implementation", submittedAt: "4 hours ago", status: "pending" },
    { studentName: "Peter Msigwa", course: "Data Structures & Algorithms", assignment: "Binary Tree Implementation", submittedAt: "1 day ago", status: "reviewed" },
    { studentName: "Fatuma Hassan", course: "Advanced Database Systems", assignment: "Query Optimization Report", submittedAt: "2 days ago", status: "pending" }
  ];

  const upcomingSessions = [
    { title: "Advanced Database Systems - Lecture 8", course: "CS 401", date: "Dec 12, 2024", time: "10:00 AM - 12:00 PM", location: "Room 201, CS Building", type: "lecture" },
    { title: "Data Structures Lab Session", course: "CS 201", date: "Dec 13, 2024", time: "2:00 PM - 4:00 PM", location: "Computer Lab 1", type: "lab" },
    { title: "ML Project Presentations", course: "CS 451", date: "Dec 14, 2024", time: "9:00 AM - 11:00 AM", location: "Conference Hall", type: "presentation" }
  ];

  return (
    <div className="container py-8 space-y-8 animate-fade-in">
      {/* Welcome Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold">Welcome back, {instructor.profile.full_name}! 👋</h1>
          <div className="flex items-center gap-4 text-muted-foreground">
            <span>ID: {instructor.id}</span>
            <span>•</span>
            <span>Status: {instructor.is_active ? "Active" : "Inactive"}</span>
            <span>•</span>
            <span>Role: {instructor.profile.permission}</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button asChild variant="outline" size="sm">
            <Link to="/instructor/schedule">
              <Calendar className="mr-2 h-4 w-4" />
              View Schedule
            </Link>
          </Button>
          <Button asChild size="sm">
            <Link to="/instructor/create-course">
              <Plus className="mr-2 h-4 w-4" />
              Create Course
            </Link>
          </Button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <Card key={index} className="hover:shadow-academic transition-all duration-300">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">{stat.title}</CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold mb-1">{stat.value}</div>
              <p className="text-xs text-muted-foreground mb-2">{stat.description}</p>
              <div className="flex items-center text-xs text-success">
                <TrendingUp className="mr-1 h-3 w-3" />
                {stat.trend}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* My Courses */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5" />
                My Courses
              </CardTitle>
              <CardDescription>Manage and monitor your courses</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {courses.map(course => (
                <div key={course.id} className="flex items-center justify-between p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors">
                  <div className="flex-1 space-y-2">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-semibold">{course.title}</h3>
                        <p className="text-sm text-muted-foreground">{course.code}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant={course.status === 'published' ? 'default' : 'secondary'}>{course.status}</Badge>
                        <Badge variant="outline" className="text-xs">{course.students} students</Badge>
                      </div>
                    </div>
                    <Progress value={course.progress} className="h-2" />
                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span>Next: {course.nextSession}</span>
                      <span>{course.pendingSubmissions} pending submissions</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 ml-4">
                    <Button asChild size="sm" variant="outline">
                      <Link to={`/course/${course.id}`}>
                        <Eye className="mr-2 h-4 w-4" />
                        View
                      </Link>
                    </Button>
                    <Button asChild size="sm">
                      <Link to={`/instructor/course/${course.id}/manage`}>
                        <Edit className="mr-2 h-4 w-4" />
                        Manage
                      </Link>
                    </Button>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Recent Submissions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><FileText className="h-5 w-5" />Recent Submissions</CardTitle>
              <CardDescription>Student assignments waiting for review</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentSubmissions.map((submission, index) => (
                  <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-card-subtle">
                    <div className="space-y-1">
                      <p className="font-medium">{submission.studentName}</p>
                      <p className="text-sm text-muted-foreground">{submission.assignment}</p>
                      <p className="text-xs text-muted-foreground">{submission.course}</p>
                      <p className="text-xs text-muted-foreground">Submitted {submission.submittedAt}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge className={submission.status === 'pending' ? 'bg-warning text-warning-foreground' : 'bg-success text-success-foreground'}>
                        {submission.status}
                      </Badge>
                      <Button asChild size="sm" variant="outline">
                        <Link to="/instructor/review">Review</Link>
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Upcoming Sessions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><Calendar className="h-5 w-5" />Upcoming Sessions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {upcomingSessions.map((session, index) => (
                <div key={index} className="space-y-2 p-3 rounded-lg bg-card-subtle">
                  <div className="flex items-center justify-between">
                    <h4 className="text-sm font-medium">{session.title}</h4>
                    <Badge variant="secondary" className="text-xs">{session.type}</Badge>
                  </div>
                  <p className="text-xs text-muted-foreground">{session.course}</p>
                  <div className="text-xs text-muted-foreground">
                    <p>{session.date} • {session.time}</p>
                    <p>{session.location}</p>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
