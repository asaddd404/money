import { useMutation, useQuery } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { endpoints } from '@/api/endpoints';
import { http, postWithIdempotency } from '@/api/http';
import { PageHeader } from '@/components/common';
import { EnrollmentCard, EnrollmentRow } from '@/components/entity-cards';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

interface GroupItem {
  id: string;
  name: string;
}

interface EnrollmentItem {
  student_id: string;
  group_id: string;
  student_name: string;
}

interface EnrollmentAction {
  studentId: string;
  groupId: string;
  kind: 'approve' | 'reject';
}

interface AwardPayload {
  student_id: string;
  group_id: string;
  amount: number;
  reason: string;
}

export const TeacherHomePage = () => {
  const { data } = useQuery<{ items: GroupItem[] }>({
    queryKey: ['teacher-home'],
    queryFn: async () =>
      (await http.get('/groups', { params: { limit: 20, offset: 0 } })).data
  });
  return (
    <div className="space-y-3">
      <PageHeader title="Teacher Home" />
      {(data?.items ?? []).map((g) => (
        <div className="rounded-xl border p-4" key={g.id}>
          {g.name}
        </div>
      ))}
    </div>
  );
};

export const TeacherGroupsPage = () => {
  const { data } = useQuery<{ items: GroupItem[] }>({
    queryKey: ['teacher-groups'],
    queryFn: async () => (await http.get(endpoints.groups)).data
  });
  return (
    <div className="space-y-3">
      <PageHeader title="My groups" />
      {(data?.items ?? []).map((g) => (
        <div className="rounded-xl border p-4" key={g.id}>
          {g.name}
        </div>
      ))}
    </div>
  );
};

export const TeacherEnrollmentsPage = () => {
  const { data } = useQuery<{ items: EnrollmentItem[] }>({
    queryKey: ['pending-enrollments'],
    queryFn: async () =>
      (
        await http.get('/groups/current/enrollments', {
          params: { status: 'pending' }
        })
      ).data
  });
  const action = useMutation({
    mutationFn: ({ studentId, groupId, kind }: EnrollmentAction) =>
      http.post(`/enrollments/${studentId}/${groupId}/${kind}`)
  });
  return (
    <div className="space-y-3">
      <PageHeader title="Pending enrollments" />
      {(data?.items ?? []).map((e) => (
        <EnrollmentCard
          key={e.student_id}
          name={e.student_name}
          onApprove={() =>
            action.mutate({
              studentId: e.student_id,
              groupId: e.group_id,
              kind: 'approve'
            })
          }
          onReject={() =>
            action.mutate({
              studentId: e.student_id,
              groupId: e.group_id,
              kind: 'reject'
            })
          }
        />
      ))}
      <div>
        {(data?.items ?? []).map((e) => (
          <EnrollmentRow
            key={`${e.student_id}-row`}
            name={e.student_name}
            onApprove={() =>
              action.mutate({
                studentId: e.student_id,
                groupId: e.group_id,
                kind: 'approve'
              })
            }
            onReject={() =>
              action.mutate({
                studentId: e.student_id,
                groupId: e.group_id,
                kind: 'reject'
              })
            }
          />
        ))}
      </div>
    </div>
  );
};

export const TeacherAwardPage = () => {
  const { register, handleSubmit } = useForm<AwardPayload>();
  const award = useMutation({
    mutationFn: (data: AwardPayload) =>
      postWithIdempotency(endpoints.awards, data)
  });
  return (
    <form className="space-y-3" onSubmit={handleSubmit((v) => award.mutate(v))}>
      <PageHeader title="Award coins" />
      <Input placeholder="Student ID" {...register('student_id')} />
      <Input placeholder="Group ID" {...register('group_id')} />
      <Input
        type="number"
        placeholder="Amount"
        {...register('amount', { valueAsNumber: true })}
      />
      <Input placeholder="Reason" {...register('reason')} />
      <Button className="w-full" disabled={award.isPending}>
        {award.isPending ? 'Pending...' : 'Award'}
      </Button>
    </form>
  );
};

export const TeacherLeaderboardsPage = () => (
  <div className="space-y-3">
    <PageHeader title="Group leaderboard" />
    <p className="rounded-xl border p-4 text-sm text-muted-foreground">
      Use student leaderboard analytics scoped for teacher groups.
    </p>
  </div>
);
