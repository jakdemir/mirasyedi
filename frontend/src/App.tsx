import React, { useState } from 'react';
import { Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Step1Form from './components/form/Step1Form';
import Step3Form from './components/form/Step3Form';
import ResultView from './components/shared/ResultView';
import { FormStep1Data, FormStep3Data, InheritanceResponse, ParentType, FamilyNode } from './types';
import { inheritanceApi } from './services/api';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
  },
});

const queryClient = new QueryClient();

const App: React.FC = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<{
    step1?: FormStep1Data;
    step3?: FormStep3Data;
  }>({});
  const [result, setResult] = useState<InheritanceResponse | null>(null);
  const [currentDegree, setCurrentDegree] = useState<1 | 2 | 3>(1);

  const handleStep1Submit = (data: FormStep1Data) => {
    setFormData((prev) => ({ ...prev, step1: data }));
    setStep(2);
  };

  const handleNoChildren = () => {
    setCurrentDegree(2);
    setFormData((prev) => ({ ...prev, step3: undefined }));
  };

  const handleNoParents = () => {
    setCurrentDegree(3);
    setFormData((prev) => ({ ...prev, step3: undefined }));
  };

  const createFamilyNode = (data: FormStep3Data): FamilyNode => {
    const baseNode: FamilyNode = {
      person: {
        id: 'deceased',
        name: 'Deceased',
        is_alive: false,
        share: 0,
      },
      spouse: formData.step1?.has_spouse
        ? {
            id: 'spouse',
            name: formData.step1.spouse_name || '',
            is_alive: formData.step1.spouse_is_alive,
            marriage_info: {
              marriage_order: 1,
              is_current: true,
            },
            share: 0,
          }
        : undefined,
      children: [],
      parents: {},
    };

    switch (data.degree) {
      case 1:
        if (data.firstDegree?.children.length) {
          baseNode.children = data.firstDegree.children.map((child) => ({
            person: {
              id: child.id,
              name: child.name,
              is_alive: child.is_alive,
              parent_id: 'deceased',
              share: 0,
            },
            children: [],
            parents: {},
          }));
        }
        break;

      case 2: {
        const secondDegree = data.secondDegree;
        if (secondDegree?.mother || secondDegree?.father) {
          const parents: { [key in ParentType]?: FamilyNode } = {};
          const siblings = secondDegree.siblings || [];

          if (secondDegree.mother) {
            parents[ParentType.MOTHER] = {
              person: {
                id: secondDegree.mother.id,
                name: secondDegree.mother.name,
                is_alive: secondDegree.mother.is_alive,
                share: 0,
              },
              children: siblings.map((sibling) => ({
                person: {
                  id: sibling.id,
                  name: sibling.name,
                  is_alive: sibling.is_alive,
                  parent_id: secondDegree.mother?.id,
                  share: 0,
                },
                children: [],
                parents: {},
              })),
              parents: {},
            };
          }

          if (secondDegree.father) {
            parents[ParentType.FATHER] = {
              person: {
                id: secondDegree.father.id,
                name: secondDegree.father.name,
                is_alive: secondDegree.father.is_alive,
                share: 0,
              },
              children: siblings.map((sibling) => ({
                person: {
                  id: sibling.id,
                  name: sibling.name,
                  is_alive: sibling.is_alive,
                  parent_id: secondDegree.father?.id,
                  share: 0,
                },
                children: [],
                parents: {},
              })),
              parents: {},
            };
          }

          baseNode.parents = parents;
        }
        break;
      }

      case 3: {
        const thirdDegree = data.thirdDegree;
        if (thirdDegree?.maternal || thirdDegree?.paternal) {
          const parents: { [key in ParentType]?: FamilyNode } = {};

          // Maternal side
          if (thirdDegree.maternal?.grandmother || thirdDegree.maternal?.grandfather) {
            const maternalParents: { [key in ParentType]?: FamilyNode } = {};
            const maternalUncles = thirdDegree.maternal.uncles || [];

            if (thirdDegree.maternal.grandmother) {
              maternalParents[ParentType.MOTHER] = {
                person: {
                  id: thirdDegree.maternal.grandmother.id,
                  name: thirdDegree.maternal.grandmother.name,
                  is_alive: thirdDegree.maternal.grandmother.is_alive,
                  share: 0,
                },
                children: [],
                parents: {},
              };
            }

            if (thirdDegree.maternal.grandfather) {
              maternalParents[ParentType.FATHER] = {
                person: {
                  id: thirdDegree.maternal.grandfather.id,
                  name: thirdDegree.maternal.grandfather.name,
                  is_alive: thirdDegree.maternal.grandfather.is_alive,
                  share: 0,
                },
                children: maternalUncles.map((uncle) => ({
                  person: {
                    id: uncle.id,
                    name: uncle.name,
                    is_alive: uncle.is_alive,
                    parent_id: thirdDegree.maternal.grandfather?.id,
                    share: 0,
                  },
                  children: [],
                  parents: {},
                })),
                parents: {},
              };
            }

            parents[ParentType.MOTHER] = {
              person: {
                id: 'deceased-mother',
                name: 'Deceased Mother',
                is_alive: false,
                share: 0,
              },
              children: [],
              parents: maternalParents,
            };
          }

          // Paternal side
          if (thirdDegree.paternal?.grandmother || thirdDegree.paternal?.grandfather) {
            const paternalParents: { [key in ParentType]?: FamilyNode } = {};
            const paternalUncles = thirdDegree.paternal.uncles || [];

            if (thirdDegree.paternal.grandmother) {
              paternalParents[ParentType.MOTHER] = {
                person: {
                  id: thirdDegree.paternal.grandmother.id,
                  name: thirdDegree.paternal.grandmother.name,
                  is_alive: thirdDegree.paternal.grandmother.is_alive,
                  share: 0,
                },
                children: [],
                parents: {},
              };
            }

            if (thirdDegree.paternal.grandfather) {
              paternalParents[ParentType.FATHER] = {
                person: {
                  id: thirdDegree.paternal.grandfather.id,
                  name: thirdDegree.paternal.grandfather.name,
                  is_alive: thirdDegree.paternal.grandfather.is_alive,
                  share: 0,
                },
                children: paternalUncles.map((uncle) => ({
                  person: {
                    id: uncle.id,
                    name: uncle.name,
                    is_alive: uncle.is_alive,
                    parent_id: thirdDegree.paternal.grandfather?.id,
                    share: 0,
                  },
                  children: [],
                  parents: {},
                })),
                parents: {},
              };
            }

            parents[ParentType.FATHER] = {
              person: {
                id: 'deceased-father',
                name: 'Deceased Father',
                is_alive: false,
                share: 0,
              },
              children: [],
              parents: paternalParents,
            };
          }

          baseNode.parents = parents;
        }
        break;
      }
    }

    return baseNode;
  };

  const handleStep3Submit = async (data: FormStep3Data) => {
    setFormData((prev) => ({ ...prev, step3: data }));
    
    if (!formData.step1) return;

    try {
      const familyTree = createFamilyNode(data);
      const request = {
        estate_value: formData.step1.estate_value,
        family_tree: familyTree,
      };

      console.log('Sending request:', JSON.stringify(request, null, 2));
      const response = await inheritanceApi.calculateInheritance(request);
      setResult(response);
    } catch (error) {
      console.error('Failed to calculate inheritance:', error);
    }
  };

  const handleReset = () => {
    setStep(1);
    setCurrentDegree(1);
    setFormData({});
    setResult(null);
  };

  if (result) {
    return <ResultView result={result} onReset={handleReset} />;
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <QueryClientProvider client={queryClient}>
        <Container>
          {step === 1 && (
            <Step1Form
              onSubmit={handleStep1Submit}
              defaultValues={formData.step1}
            />
          )}
          {step === 2 && (
            <Step3Form
              degree={currentDegree}
              onSubmit={handleStep3Submit}
              onBack={() => setStep(1)}
              defaultValues={formData.step3}
              onNoHeirs={currentDegree === 1 ? handleNoChildren : currentDegree === 2 ? handleNoParents : undefined}
              spouseData={formData.step1}
            />
          )}
        </Container>
      </QueryClientProvider>
    </ThemeProvider>
  );
};

export default App;
