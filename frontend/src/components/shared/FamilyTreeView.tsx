import React from 'react';
import { Box, Paper, Typography, Stack } from '@mui/material';
import { FamilyNode, familyTreeColors, RelativeType } from '../../types';

interface FamilyTreeNodeProps {
  node: FamilyNode;
  level?: number;
  type: RelativeType | 'deceased';
}

const FamilyTreeNode: React.FC<FamilyTreeNodeProps> = ({ node, level = 0, type }) => {
  const getNodeColor = () => {
    if (!node.person.is_alive) {
      switch (type) {
        case 'child':
          return familyTreeColors.childDeceased;
        case 'parent':
          return familyTreeColors.parentDeceased;
        case 'grandparent':
          return familyTreeColors.grandparentDeceased;
        default:
          return familyTreeColors.deceased;
      }
    }
    return familyTreeColors[type];
  };

  return (
    <Box sx={{ ml: level * 4, mb: 2 }}>
      <Paper
        elevation={2}
        sx={{
          p: 2,
          bgcolor: getNodeColor(),
          borderRadius: 2,
          maxWidth: 'fit-content',
        }}
      >
        <Stack spacing={1}>
          <Typography variant="subtitle1" fontWeight="bold">
            {node.person.name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {!node.person.is_alive && '(Deceased)'}
            {node.person.share > 0 && ` - Share: ${node.person.share.toLocaleString('tr-TR')} TRY`}
            {node.person.share_percentage && ` (${node.person.share_percentage.toFixed(2)}%)`}
          </Typography>
        </Stack>
      </Paper>

      {node.spouse && (
        <Box sx={{ ml: 4, mt: 1 }}>
          <Paper
            elevation={2}
            sx={{
              p: 2,
              bgcolor: familyTreeColors.spouse,
              borderRadius: 2,
              maxWidth: 'fit-content',
            }}
          >
            <Stack spacing={1}>
              <Typography variant="subtitle1" fontWeight="bold">
                {node.spouse.name} (Spouse)
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {node.spouse.share > 0 && `Share: ${node.spouse.share.toLocaleString('tr-TR')} TRY`}
                {node.spouse.share_percentage && ` (${node.spouse.share_percentage.toFixed(2)}%)`}
              </Typography>
            </Stack>
          </Paper>
        </Box>
      )}

      {node.children.length > 0 && (
        <Box sx={{ mt: 2 }}>
          {node.children.map((child, index) => (
            <FamilyTreeNode
              key={child.person.id}
              node={child}
              level={level + 1}
              type={type === 'deceased' ? 'child' : type}
            />
          ))}
        </Box>
      )}
    </Box>
  );
};

interface FamilyTreeViewProps {
  familyTree: FamilyNode;
  type: RelativeType | 'deceased';
}

const FamilyTreeView: React.FC<FamilyTreeViewProps> = ({ familyTree, type }) => {
  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Family Tree
      </Typography>
      <FamilyTreeNode node={familyTree} type={type} />
    </Box>
  );
};

export default FamilyTreeView; 