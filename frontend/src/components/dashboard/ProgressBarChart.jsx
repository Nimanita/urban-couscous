// src/components/dashboard/ProgressBarChart.jsx
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';

const ProgressBarChart = ({ data }) => {
  const colors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b'];

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Course Progress
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="course_name"
            stroke="#6b7280"
            fontSize={12}
            tickLine={false}
            angle={-15}
            textAnchor="end"
            height={80}
          />
          <YAxis
            stroke="#6b7280"
            fontSize={12}
            tickLine={false}
            label={{ value: 'Progress %', angle: -90, position: 'insideLeft' }}
            domain={[0, 100]}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
            }}
            formatter={(value) => [`${value}%`, 'Progress']}
          />
          <Bar dataKey="progress" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ProgressBarChart;