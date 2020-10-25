import { Layout, Row, Col } from 'antd';
import Search from './Search';

const { Content } = Layout;

function App() {
  return (
    <Layout>
      <Content
        style={{
          padding: 24,
          minHeight: '100vh',
        }}>
        <Row>
          <Col span={12} offset={6}>
            <Search />
          </Col>
        </Row>
      </Content>
    </Layout>
  );
}

export default App;
