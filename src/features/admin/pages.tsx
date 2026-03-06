import { useMutation, useQuery } from '@tanstack/react-query';
import { endpoints } from '@/api/endpoints';
import { http } from '@/api/http';
import { PageHeader } from '@/components/common';
import { Button } from '@/components/ui/button';

interface TeacherPolicyItem {
  teacher_id: string;
  teacher_name: string;
  daily_limit: number;
}

export const AdminHomePage = () => (
  <div className="space-y-2">
    <PageHeader title="Admin Home" />
    <p className="rounded-xl border p-4">Full platform control center.</p>
  </div>
);

export const AdminPoliciesPage = () => {
  const { data, refetch } = useQuery<{ items: TeacherPolicyItem[] }>({
    queryKey: ['teacher-policies'],
    queryFn: async () => (await http.get(endpoints.admin.teacherPolicies)).data
  });
  const patch = useMutation({
    mutationFn: ({
      teacherId,
      daily_limit
    }: {
      teacherId: string;
      daily_limit: number;
    }) =>
      http.patch(`${endpoints.admin.teacherPolicies}/${teacherId}`, {
        daily_limit
      }),
    onSuccess: () => refetch()
  });
  return (
    <div className="space-y-3">
      <PageHeader title="Teacher policies" />
      {(data?.items ?? []).map((p) => (
        <div key={p.teacher_id} className="rounded-xl border p-4">
          <p>{p.teacher_name}</p>
          <Button
            className="mt-2"
            onClick={() =>
              patch.mutate({
                teacherId: p.teacher_id,
                daily_limit: p.daily_limit + 10
              })
            }
          >
            Increase +10
          </Button>
        </div>
      ))}
    </div>
  );
};
