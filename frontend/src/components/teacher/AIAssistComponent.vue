<template>
  <v-dialog v-model="showDialog" max-width="800px" persistent>
    <v-card>
      <!-- Header -->
      <v-card-title class="bg-primary text-white">
        <v-icon start>mdi-robot</v-icon>
        AI-Assisted Module Creator
        <v-spacer></v-spacer>
        <v-btn icon @click="closeDialog" variant="text">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text class="pa-6">
        <!-- AI Assisted Workflow Info -->
        <v-alert type="info" variant="tonal" class="mb-6">
          <v-icon start>mdi-lightbulb</v-icon>
          <strong>AI Assisted Workflow:</strong> Create engaging educational modules with AI assistance. 
          Our AI will generate comprehensive content including sections, activities, and assessments.
        </v-alert>

        <!-- Form -->
        <v-form @submit.prevent="generateModule" ref="form">
          <v-row>
            <!-- Module Topic -->
            <v-col cols="12">
              <v-text-field
                v-model="formData.topic"
                label="Module Topic"
                placeholder="e.g., Advanced Budgeting for Teenagers"
                variant="outlined"
                :rules="[v => !!v || 'Topic is required']"
                required
              ></v-text-field>
            </v-col>

            <!-- Target Age Group -->
            <v-col cols="12" md="6">
              <v-select
                v-model="formData.ageGroup"
                label="Target Age Group"
                :items="ageGroups"
                item-title="label"
                item-value="value"
                variant="outlined"
                required
              ></v-select>
            </v-col>

            <!-- Estimated Duration -->
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.duration"
                label="Estimated Duration"
                placeholder="e.g., 45 minutes"
                variant="outlined"
                :rules="[v => !!v || 'Duration is required']"
                required
              >
                <template #append>
                  <v-icon>mdi-clock-outline</v-icon>
                </template>
              </v-text-field>
            </v-col>

            <!-- Generate Button -->
            <v-col cols="12">
              <v-btn
                @click="generateModule"
                :loading="loading"
                :disabled="!formData.topic || !formData.duration"
                color="primary"
                size="large"
                block
                class="mt-4"
              >
                <v-icon start>mdi-magic-staff</v-icon>
                {{ loading ? 'Generating Module...' : 'Generate Module with AI' }}
              </v-btn>
            </v-col>
          </v-row>
        </v-form>

        <!-- Error Display -->
        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          class="mt-4"
          closable
          @click:close="error = ''"
        >
          {{ error }}
        </v-alert>

        <!-- Generated Module Display -->
        <div v-if="generatedModule" class="mt-6">
          <v-card variant="outlined" class="pa-4">
            <div class="d-flex justify-space-between align-center mb-4">
              <h3 class="text-h6 text-primary">Generated Module</h3>
              <v-btn
                @click="generateFullModule"
                :loading="loadingFull"
                :disabled="loadingFull"
                color="secondary"
                size="small"
              >
                <v-icon start>mdi-plus</v-icon>
                {{ loadingFull ? 'Generating...' : 'Generate Full Module' }}
              </v-btn>
            </div>

            <!-- Module Basic Info -->
            <v-card variant="tonal" class="pa-4 mb-4">
              <h4 class="text-h5 font-weight-bold mb-2">{{ generatedModule.title }}</h4>
              <v-chip
                :color="getDifficultyColor(generatedModule.difficulty)"
                size="small"
                class="mb-2"
              >
                {{ generatedModule.difficulty }}
              </v-chip>
              <p class="text-body-1 mb-3">{{ generatedModule.description }}</p>
              
              <v-row>
                <v-col cols="6">
                  <div class="text-caption text-medium-emphasis">Duration:</div>
                  <div class="text-body-2">{{ generatedModule.duration }}</div>
                </v-col>
                <v-col cols="6">
                  <div class="text-caption text-medium-emphasis">Age Group:</div>
                  <div class="text-body-2">{{ generatedModule.targetAge }}</div>
                </v-col>
              </v-row>

              <!-- Learning Objectives -->
              <div v-if="generatedModule.learningObjectives" class="mt-4">
                <h5 class="text-subtitle-1 font-weight-medium mb-2">Learning Objectives:</h5>
                <v-list density="compact" class="bg-transparent">
                  <v-list-item
                    v-for="(objective, index) in generatedModule.learningObjectives"
                    :key="index"
                    class="pa-0"
                  >
                    <template #prepend>
                      <v-icon size="small" color="primary">mdi-check-circle</v-icon>
                    </template>
                    <v-list-item-title class="text-body-2">{{ objective }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </div>
            </v-card>

            <!-- Full Module Content -->
            <div v-if="fullModuleContent">
              <!-- Module Sections -->
              <div v-if="fullModuleContent.sections" class="mb-6">
                <h5 class="text-subtitle-1 font-weight-medium mb-3">Module Sections:</h5>
                <v-expansion-panels variant="accordion">
                  <v-expansion-panel
                    v-for="(section, index) in fullModuleContent.sections"
                    :key="index"
                  >
                    <v-expansion-panel-title>
                      <div class="d-flex align-center">
                        <v-icon
                          :icon="getSectionIcon(section.type)"
                          color="primary"
                          class="mr-3"
                        ></v-icon>
                        <span class="font-weight-medium">{{ section.title }}</span>
                        <v-chip size="x-small" class="ml-auto">{{ section.duration }}</v-chip>
                      </div>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                      <p class="text-body-2">{{ section.content }}</p>
                      <v-chip
                        :color="getSectionTypeColor(section.type)"
                        size="small"
                        class="mt-2"
                      >
                        {{ section.type }}
                      </v-chip>
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </div>

              <!-- Learning Activities -->
              <div v-if="fullModuleContent.activities" class="mb-6">
                <h5 class="text-subtitle-1 font-weight-medium mb-3">Learning Activities:</h5>
                <v-row>
                  <v-col
                    v-for="(activity, index) in fullModuleContent.activities"
                    :key="index"
                    cols="12"
                    md="6"
                  >
                    <v-card variant="outlined" class="pa-3">
                      <div class="d-flex align-center mb-2">
                        <v-icon
                          :icon="getActivityIcon(activity.type)"
                          color="orange"
                          class="mr-2"
                        ></v-icon>
                        <h6 class="text-subtitle-2 font-weight-medium">{{ activity.title }}</h6>
                      </div>
                      <p class="text-body-2 mb-2">{{ activity.description }}</p>
                      <div class="d-flex justify-space-between align-center">
                        <v-chip size="x-small" color="orange">{{ activity.type }}</v-chip>
                        <span class="text-caption">{{ activity.duration }}</span>
                      </div>
                    </v-card>
                  </v-col>
                </v-row>
              </div>

              <!-- Quiz Questions -->
              <div v-if="fullModuleContent.quiz">
                <h5 class="text-subtitle-1 font-weight-medium mb-3">Quiz Questions:</h5>
                <v-expansion-panels variant="accordion">
                  <v-expansion-panel
                    v-for="(question, index) in fullModuleContent.quiz"
                    :key="index"
                  >
                    <v-expansion-panel-title>
                      <div class="d-flex align-center">
                        <v-icon color="blue" class="mr-3">mdi-help-circle</v-icon>
                        <span class="font-weight-medium">Q{{ index + 1 }}: {{ question.question }}</span>
                      </div>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                      <v-radio-group v-model="question.selectedAnswer" readonly>
                        <v-radio
                          v-for="(option, optIndex) in question.options"
                          :key="optIndex"
                          :label="`${String.fromCharCode(65 + optIndex)}. ${option.text}`"
                          :value="optIndex"
                          :color="option.isCorrect ? 'success' : 'default'"
                        ></v-radio>
                      </v-radio-group>
                      <v-alert
                        v-if="question.explanation"
                        type="info"
                        variant="tonal"
                        class="mt-3"
                        density="compact"
                      >
                        <strong>Explanation:</strong> {{ question.explanation }}
                      </v-alert>
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </div>
            </div>

            <!-- Save Module Button -->
            <div class="d-flex gap-3 mt-6">
              <v-btn
                @click="saveModule"
                :loading="saving"
                :disabled="!generatedModule"
                color="success"
                size="large"
              >
                <v-icon start>mdi-content-save</v-icon>
                {{ saving ? 'Saving...' : 'Save Module' }}
              </v-btn>
              <v-btn
                @click="closeDialog"
                variant="outlined"
                size="large"
              >
                Close
              </v-btn>
            </div>
          </v-card>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useTeacherStore } from '@/stores/teacher'

// Props
interface Props {
  modelValue: boolean
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'module-saved': [module: any]
}>()

// Store
const teacherStore = useTeacherStore()

// Reactive state
const loading = ref(false)
const loadingFull = ref(false)
const saving = ref(false)
const error = ref('')
const generatedModule = ref<any>(null)
const fullModuleContent = ref<any>(null)
const form = ref<any>(null)

// Form data
const formData = reactive({
  topic: '',
  ageGroup: '11-14',
  duration: '45 minutes'
})

// Age group options
const ageGroups = [
  { label: '8-10 years', value: '8-10' },
  { label: '11-14 years', value: '11-14' },
  { label: '15-18 years', value: '15-18' }
]

// Computed
const showDialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Methods
const closeDialog = () => {
  showDialog.value = false
  resetForm()
}

const resetForm = () => {
  formData.topic = ''
  formData.ageGroup = '11-14'
  formData.duration = '45 minutes'
  error.value = ''
  generatedModule.value = null
  fullModuleContent.value = null
}

const getDifficultyColor = (difficulty: string) => {
  switch (difficulty) {
    case 'beginner': return 'success'
    case 'intermediate': return 'warning'
    case 'advanced': return 'error'
    default: return 'primary'
  }
}

const getSectionIcon = (type: string) => {
  switch (type) {
    case 'lesson': return 'mdi-book-open-variant'
    case 'reading': return 'mdi-file-document'
    case 'video': return 'mdi-video'
    case 'discussion': return 'mdi-forum'
    default: return 'mdi-book'
  }
}

const getSectionTypeColor = (type: string) => {
  switch (type) {
    case 'lesson': return 'primary'
    case 'reading': return 'info'
    case 'video': return 'purple'
    case 'discussion': return 'orange'
    default: return 'grey'
  }
}

const getActivityIcon = (type: string) => {
  switch (type) {
    case 'exercise': return 'mdi-dumbbell'
    case 'simulation': return 'mdi-gamepad-variant'
    case 'case_study': return 'mdi-briefcase'
    case 'group_work': return 'mdi-account-group'
    case 'project': return 'mdi-folder-multiple'
    default: return 'mdi-lightbulb'
  }
}

const generateModule = async () => {
  if (!formData.topic.trim()) {
    error.value = 'Please enter a module topic'
    return
  }

  loading.value = true
  error.value = ''
  generatedModule.value = null
  fullModuleContent.value = null

  try {
    console.log('🤖 [AI ASSIST] Generating module...')
    
    // Initialize Cerebras client with environment variable
    const cerebras = new (await import('@cerebras/cerebras_cloud_sdk')).default({
      apiKey: import.meta.env.VITE_CEREBRAS_API_KEY
    })

    // JSON Schema for structured output (Cerebras compatible)
    const moduleSchema = {
      type: "object",
      properties: {
        title: {
          type: "string"
        },
        difficulty: {
          type: "string",
          enum: ["beginner", "intermediate", "advanced"]
        },
        description: {
          type: "string"
        },
        duration: {
          type: "string"
        },
        targetAge: {
          type: "string"
        },
        learningObjectives: {
          type: "array",
          items: {
            type: "string"
          }
        },
        prerequisites: {
          type: "array",
          items: {
            type: "string"
          }
        },
        keyTopics: {
          type: "array",
          items: {
            type: "string"
          }
        }
      },
      required: ["title", "difficulty", "description", "duration", "targetAge", "learningObjectives"],
      additionalProperties: false
    }

    // Create the prompt for generating educational modules
    const systemPrompt = `You are an expert educational curriculum designer specializing in creating engaging, age-appropriate learning modules for teachers. Your task is to design comprehensive educational modules that are pedagogically sound and practically implementable.

Guidelines for module creation:
- Make content age-appropriate and engaging for the specified age group
- Ensure learning objectives are specific, measurable, and achievable
- Create clear, concise descriptions that teachers can easily understand and implement
- Consider different learning styles and abilities
- Align with common educational standards and best practices
- Make modules practical and actionable for classroom use

Focus on creating modules that are:
- Clear and well-structured
- Engaging and interactive
- Educationally valuable
- Practical for teachers to implement
- Appropriate for the specified duration and age group`

    const userPrompt = `Create an educational module with the following specifications:

Topic: ${formData.topic}
Target Age Group: ${formData.ageGroup} years old
Estimated Duration: ${formData.duration}

Please design a complete educational module that includes:
1. An engaging title that captures student interest
2. Appropriate difficulty level for the age group
3. A clear, compelling description of what students will learn
4. Specific learning objectives that are measurable and achievable
5. Key topics that will be covered
6. Any prerequisites or prior knowledge needed

Ensure the module is practical, engaging, and educationally sound for teachers to implement in their classrooms.`

    const completionResponse = await cerebras.chat.completions.create({
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt }
      ],
      model: 'qwen-3-235b-a22b-instruct-2507',
      stream: false,
      max_completion_tokens: 40000,
      temperature: 0.6,
      top_p: 0.95,
      response_format: {
        type: "json_schema",
        json_schema: {
          name: "educational_module",
          strict: true,
          schema: moduleSchema
        }
      }
    })

    // Parse the structured response
    const moduleData = JSON.parse(completionResponse.choices[0].message.content)
    generatedModule.value = moduleData
    
    console.log('✅ [AI ASSIST] Module generated successfully')
    
  } catch (err: any) {
    error.value = `Error generating module: ${err.message}`
    console.error('❌ [AI ASSIST] Generation failed:', err)
  } finally {
    loading.value = false
  }
}

const generateFullModule = async () => {
  if (!generatedModule.value) return

  loadingFull.value = true
  error.value = ''
  
  try {
    console.log('🤖 [AI ASSIST] Generating full module content...')
    
    const moduleInfo = generatedModule.value
    
    // Initialize Cerebras client
    const cerebras = new (await import('@cerebras/cerebras_cloud_sdk')).default({
      apiKey: import.meta.env.VITE_CEREBRAS_API_KEY
    })

    // Schema for detailed module sections
    const sectionsSchema = {
      type: "object",
      properties: {
        sections: {
          type: "array",
          items: {
            type: "object",
            properties: {
              title: { type: "string" },
              type: { type: "string", enum: ["lesson", "reading", "video", "discussion"] },
              content: { type: "string" },
              duration: { type: "string" },
              orderIndex: { type: "integer" }
            },
            required: ["title", "type", "content", "duration"],
            additionalProperties: false
          }
        }
      },
      required: ["sections"],
      additionalProperties: false
    }

    // Schema for learning activities
    const activitiesSchema = {
      type: "object",
      properties: {
        activities: {
          type: "array",
          items: {
            type: "object",
            properties: {
              title: { type: "string" },
              type: { type: "string", enum: ["exercise", "simulation", "case_study", "group_work", "project"] },
              description: { type: "string" },
              duration: { type: "string" },
              materials: { type: "string" }
            },
            required: ["title", "type", "description", "duration"],
            additionalProperties: false
          }
        }
      },
      required: ["activities"],
      additionalProperties: false
    }

    // Schema for quiz questions
    const quizSchema = {
      type: "object",
      properties: {
        quiz: {
          type: "array",
          items: {
            type: "object",
            properties: {
              question: { type: "string" },
              type: { type: "string", enum: ["multiple_choice", "true_false"] },
              options: {
                type: "array",
                items: {
                  type: "object",
                  properties: {
                    text: { type: "string" },
                    isCorrect: { type: "boolean" }
                  },
                  required: ["text", "isCorrect"],
                  additionalProperties: false
                }
              },
              explanation: { type: "string" }
            },
            required: ["question", "type", "options"],
            additionalProperties: false
          }
        }
      },
      required: ["quiz"],
      additionalProperties: false
    }

    // Call 1: Generate detailed sections
    console.log('Generating module sections...')
    const sectionsResponse = await cerebras.chat.completions.create({
      messages: [
        { 
          role: "system", 
          content: `You are an expert curriculum designer. Create detailed, engaging lesson sections for educational modules.` 
        },
        { 
          role: "user", 
          content: `Create 4-5 detailed lesson sections for this module:

Title: ${moduleInfo.title}
Target Age: ${moduleInfo.targetAge}
Duration: ${moduleInfo.duration}
Difficulty: ${moduleInfo.difficulty}
Description: ${moduleInfo.description}
Learning Objectives: ${moduleInfo.learningObjectives.join(', ')}

Each section should have:
- Clear, engaging title
- Type (lesson, reading, video, or discussion)
- Detailed content description (2-3 sentences explaining what will be covered)
- Estimated duration
- Sequential order

Make the content age-appropriate and practical for teachers to implement.`
        }
      ],
      model: 'qwen-3-235b-a22b-instruct-2507',
      response_format: {
        type: "json_schema",
        json_schema: {
          name: "module_sections",
          strict: true,
          schema: sectionsSchema
        }
      }
    })

    // Call 2: Generate learning activities
    console.log('Generating learning activities...')
    const activitiesResponse = await cerebras.chat.completions.create({
      messages: [
        { 
          role: "system", 
          content: `You are an expert educational designer specializing in interactive learning activities.` 
        },
        { 
          role: "user", 
          content: `Create 3-4 engaging learning activities for this module:

Title: ${moduleInfo.title}
Target Age: ${moduleInfo.targetAge}
Learning Objectives: ${moduleInfo.learningObjectives.join(', ')}

Create diverse activity types like exercises, simulations, case studies, group work, or projects. Each activity should:
- Have a clear, engaging title
- Include detailed description of what students will do
- Specify materials needed (if any)
- Provide realistic duration
- Be age-appropriate and practical for classroom use`
        }
      ],
      model: 'qwen-3-235b-a22b-instruct-2507',
      response_format: {
        type: "json_schema",
        json_schema: {
          name: "learning_activities",
          strict: true,
          schema: activitiesSchema
        }
      }
    })

    // Call 3: Generate quiz questions
    console.log('Generating quiz questions...')
    const quizResponse = await cerebras.chat.completions.create({
      messages: [
        { 
          role: "system", 
          content: `You are an expert in educational assessment. Create high-quality quiz questions that test understanding.` 
        },
        { 
          role: "user", 
          content: `Create 4-5 quiz questions for this module:

Title: ${moduleInfo.title}
Learning Objectives: ${moduleInfo.learningObjectives.join(', ')}
Target Age: ${moduleInfo.targetAge}

Create a mix of multiple choice and true/false questions. Each question should:
- Test specific learning objectives
- Be age-appropriate and clear
- Have 3-4 realistic options for multiple choice
- Include brief explanations for correct answers
- Be neither too easy nor too difficult for the age group`
        }
      ],
      model: 'qwen-3-235b-a22b-instruct-2507',
      response_format: {
        type: "json_schema",
        json_schema: {
          name: "quiz_questions",
          strict: true,
          schema: quizSchema
        }
      }
    })

    // Parse all responses and combine
    const sections = JSON.parse(sectionsResponse.choices[0].message.content)
    const activities = JSON.parse(activitiesResponse.choices[0].message.content)
    const quiz = JSON.parse(quizResponse.choices[0].message.content)

    fullModuleContent.value = {
      sections: sections.sections,
      activities: activities.activities,
      quiz: quiz.quiz
    }

    console.log('✅ [AI ASSIST] Full module content generated!')
    
  } catch (err: any) {
    error.value = `Error generating full module: ${err.message}`
    console.error('❌ [AI ASSIST] Full generation failed:', err)
  } finally {
    loadingFull.value = false
  }
}

const saveModule = async () => {
  if (!generatedModule.value) return

  saving.value = true
  error.value = ''
  
  try {
    console.log('💾 [AI ASSIST] Saving module...')
    
    // Flatten the structure for Try Mode compatibility
    const moduleData = {
      ...generatedModule.value,
      content: `Generated by AI: ${generatedModule.value.description}`,
      // Flatten the enhanced content to top level
      sections: fullModuleContent.value?.sections || [],
      activities: fullModuleContent.value?.activities || [],
      quiz: fullModuleContent.value?.quiz || [],
      // Convert duration to number if it's a string
      duration: parseInt(generatedModule.value.duration?.replace(/\D/g, '') || '45'),
      // Set required fields
      skills: generatedModule.value.keyTopics || generatedModule.value.learningObjectives || [],
      category: 'AI Generated',
      published: true,
      createdBy: teacherStore.profile?.id || 'ai-teacher'
    }

    const savedModule = await teacherStore.addModule(moduleData)
    
    emit('module-saved', savedModule)
    closeDialog()
    
    console.log('✅ [AI ASSIST] Module saved successfully')
    
  } catch (err: any) {
    error.value = `Error saving module: ${err.response?.data?.detail || err.message}`
    console.error('❌ [AI ASSIST] Save failed:', err)
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
/* Custom styles if needed */
</style> 