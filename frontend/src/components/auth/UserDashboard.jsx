import React, { useState, useEffect } from 'react';
import { Card, Spin, notification, Descriptions, Typography } from 'antd';
import { getUserProfile } from '../../services/auth_api';

const { Title } = Typography;

const UserDashboard = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setLoading(true);
        const response = await getUserProfile();
        if (response.success) {
          setProfile(response.profile);
        } else {
          throw new Error(response.message || 'Failed to fetch profile.');
        }
      } catch (error) {
        notification.error({
          message: 'Error',
          description: error.message || 'Could not fetch user profile.',
        });
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!profile) {
    return (
      <Card>
        <Title level={4}>Could not load profile</Title>
        <p>There was an error fetching your profile data. Please try logging out and back in.</p>
      </Card>
    );
  }

  return (
    <Card>
      <Title level={3}>User Dashboard</Title>
      <Descriptions bordered column={1}>
        <Descriptions.Item label="User ID">{profile.user_id}</Descriptions.Item>
        <Descriptions.Item label="Username">{profile.username}</Descriptions.Item>
        <Descriptions.Item label="Public Key">{profile.public_key}</Descriptions.Item>
      </Descriptions>
    </Card>
  );
};

export default UserDashboard;
