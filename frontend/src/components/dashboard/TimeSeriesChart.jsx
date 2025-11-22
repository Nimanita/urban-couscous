// src/components/dashboard/TimeSeriesChart.jsx
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { format, parseISO } from 'date-fns';

const TimeSeriesChart = ({ data }) => {
  const formattedData = data.map((item) => ({
    ...item,
    formattedDate: format(parseISO(item.date), 'MMM dd'),
  }));

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Learning Activity (Last 30 Days)
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={formattedData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="formattedDate"
            stroke="#6b7280"
            fontSize={12}
            tickLine={false}
          />
          <YAxis
            stroke="#6b7280"
            fontSize={12}
            tickLine={false}
            label={{ value: 'Minutes', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
            }}
            labelStyle={{ color: '#374151', fontWeight: '500' }}
          />
          <Line
            type="monotone"
            dataKey="minutes"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={{ fill: '#3b82f6', r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TimeSeriesChart;