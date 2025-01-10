import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SpouseForm from './components/forms/SpouseForm';
import ChildrenForm from './components/forms/ChildrenForm';
import ParentsForm from './components/forms/ParentsForm';
import GrandparentsForm from './components/forms/GrandparentsForm';
import Layout from './components/Layout';
import { FamilyTreeProvider } from './context/FamilyTreeContext';

function App() {
  return (
    <FamilyTreeProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<SpouseForm />} />
            <Route path="children" element={<ChildrenForm />} />
            <Route path="parents" element={<ParentsForm />} />
            <Route path="grandparents" element={<GrandparentsForm />} />
          </Route>
        </Routes>
      </Router>
    </FamilyTreeProvider>
  );
}

export default App;
