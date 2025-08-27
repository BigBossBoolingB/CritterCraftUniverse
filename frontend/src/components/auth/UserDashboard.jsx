import React, { useState, useEffect } from 'react';
import { Card, Spin, notification, Descriptions, Typography, Button, Form, Input } from 'antd';
import { getUserProfile, updateUserProfile } from '../../services/auth_api';

const { Title } = Typography;

const UserDashboard = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [form] = Form.useForm();

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const response = await getUserProfile();
      if (response.success) {
        setProfile(response.profile);
        form.setFieldsValue(response.profile);
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

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleUpdateProfile = async (values) => {
    try {
      setLoading(true);
      const response = await updateUserProfile(values);
      if (response.success) {
        notification.success({
          message: 'Profile Updated',
          description: 'Your profile has been updated successfully.',
        });
        setIsEditing(false);
        fetchProfile(); // Refresh profile data
      } else {
        throw new Error(response.message || 'Failed to update profile.');
      }
    } catch (error) {
      notification.error({
        message: 'Update Failed',
        description: error.message,
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading && !profile) {
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
    <Card
      title={<Title level={3}>User Dashboard</Title>}
      extra={!isEditing && <Button onClick={() => setIsEditing(true)}>Edit Profile</Button>}
    >
      {isEditing ? (
        <Form
          form={form}
          layout="vertical"
          onFinish={handleUpdateProfile}
          initialValues={profile}
        >
          <Form.Item label="User ID">
            <Input value={profile.user_id} disabled />
          </Form.Item>
          <Form.Item
            name="username"
            label="Username"
            rules={[{ required: true, message: 'Please input your username!' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item label="Public Key">
            <Input value={profile.public_key} disabled />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              Save Changes
            </Button>
            <Button style={{ marginLeft: 8 }} onClick={() => setIsEditing(false)}>
              Cancel
            </Button>
          </Form.Item>
        </Form>
      ) : (
        <Descriptions bordered column={1}>
          <Descriptions.Item label="User ID">{profile.user_id}</Descriptions.Item>
          <Descriptions.Item label="Username">{profile.username}</Descriptions.Item>
          <Descriptions.Item label="Public Key">{profile.public_key}</Descriptions.Item>
        </Descriptions>
      )}
    </Card>
  );
};

export default UserDashboard;
